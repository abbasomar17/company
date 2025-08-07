from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib import messages
from django import template
from .contexts import bag_contents
from .models import *
from organisation.models import *
from django.contrib.auth.models import User
from .forms import RefundForm, CouponForm, CheckForm, AddCustomerForm, OrderForm, OrderItemForm
import stripe
import string
import random

stripe.api_key=settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


def feedback_user(request):
    offices = Office.objects.all()
    context = {
        "offices": offices
    }
    return render(request, 'home_template/user_feedback_cs.html', context)


def feedback_user_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('feedback_user')
    else:
        feedback = request.POST.get('feedback_message')
        communication = request.POST.get('communication')
        office_id = request.POST.get('office')

        office = Office.objects.get(id=office_id)

        try:
            add_feedback = FeedBack(office=office, communication=communication, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('gallery')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('feedback_user')


def products(request):
    context = {
        'items': Album.objects.all()
    }
    return render(request, "product.html", context)


def checkout(request):
    return render(request, "checkout.html")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False)
            form = CheckForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "Checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have active order")
            return redirect('checkout_view')

    def post(self, *args, **kwargs):
        form = CheckForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )
                billing_address.save()
                order.billing_address=billing_address
                order.save()
                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('payment', payment_option='paypal')
                else:
                    messages.warning(self.request,"Invalid option")
                    return redirect('checkout_view')

        except ObjectDoesNotExist:
            return redirect('checkout_view')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "You have not added billing address")
            return redirect('checkout_view')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount, #cent
                current="usd",
                source=token,
                description="Charge for abbas@gmail.com"
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amounts = order.get_total()
            payment.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()
            return redirect('/')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get(messages)}")
            return redirect('payment')

        except stripe.error.RateLimitError as e:
            messages.error(self.request, "Rate limit error")
            return redirect('payment')

        except stripe.error.InvalidRequestError as e:
            messages.error(self.request, "Invalid parameters")
            return redirect('payment')

        except stripe.error.AuthenticationError as e:
            messages.error(self.request, "Not Authenticated")
            return redirect('payment')

        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "Network error")
            return redirect('payment')

        except stripe.error.StripeError as e:
            messages.error(self.request, "Something went wrong. You were not charged please try again")
            return redirect('payment')

        except Exception as e:
            messages.error(self.request, "Serious error occurred. We have been notified.")
            return redirect('payment')


class HomeView(ListView):
    model = Album
    paginate_by = 3
    template_name = "home_template/home.html"


def gallery(request):
    list = Album.objects.filter(is_visible=True).order_by('-created')
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        albums = paginator.page(
            paginator.num_pages)  # If page is out of range (e.g.  9999), deliver last page of results.
    context = {
        'albums': list,
    }
    if 'search_query' in request.GET:
        query = request.GET.get('search_query')
        if query == '':
            p = Paginator(
                Album.objects.filter(is_visible=True).order_by('-created'),
                10
            )
            page = request.GET.get('page')
            albums = p.get_page(page)
            context = {
                'albums': list,
            }
            return render(
                request,
                'home_template/home.html',
                context
            )
        list = Album.objects.filter(
            Q(region__icontains=query) |
            Q(category__icontains=query) |
            Q(town__icontains=query) |
            Q(spec_location__icontains=query) |
            Q(labels__icontains=query)
        )
        p = Paginator(list, 10)
        page = request.GET.get('page')
        albums = p.get_page(page)
        context = {
            'albums': list,
        }
        return render(
            request,
            'home_template/home.html',
            context
        )
    return render(request, 'home_template/home.html', context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            orders = Order.objects.get(user=self.request.user.id, ordered=False)
            context = {
                'orders': orders
            }
            return render(self.request, "home_template/order_summary.html", context)
        except ObjectDoesNotExist:
            return redirect('/')


class UserOrdersView(View):
    """View for user orders page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            p = Paginator(Order.objects.filter(user=user).filter(
                ordered=False
            ), 15)
            page = request.GET.get('page')
            orders = p.get_page(page)
            return render(
                request, 'home_template/user_orders.html', {'orders': orders}
            )
        else:
            return redirect('login')


class UserOrderDetailsView(View):
    """View for user order details page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_id = kwargs['order_id']
            order = get_object_or_404(
                Order,
                id=order_id
            )
            # get order items
            order_items = OrderApartment.objects.filter(order=order)
            all_items = Order.get_order_items(order)
            # check if the order is completed

            context = {
                'order': order,
                'order_items': order_items,
                'all_items': all_items,
            }
            if order.user == request.user:
                return render(
                    request,
                    'home_template/user_order_details.html',
                    context,
                )
            else:
                return redirect('login')
        else:
            return redirect('login')


class ItemDetailView(DetailView):
    model= Album
    template_name = "home_template/product.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = AlbumImage.objects.filter(album=self.object.id)
        return context


def home(request):

    return render(request, "home.html")


def add_to_cart(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(
            Album, slug=slug
        )

        total_paid = item.real_price * 2
        ordered_date = timezone.now()
        saved_amount = item.price - item.real_price
        final_price = item.real_price * 2
        user = request.user
        rendom = Random_users.objects.get(admin__user=user)
        phone = rendom.phone
        if OrderApartment.objects.filter(item=item, user=user, ordered=False).exists():
            order_item = OrderApartment.objects.get(item=item, user=request.user, ordered=False)
            order_item.quantity += 1
            total_paid = order_item.item.real_price * order_item.quantity
            requested_quantity = order_item.quantity
            order = Order.objects.get(user=request.user)
            order.total_paid = total_paid
            order.save()
            order_item.save()
            email = NotificationRandom(
                user=rendom,
                requested_product=item,
                requested_quantity=requested_quantity,
                answer_sent=False,
            )
            email.save()
            return redirect('album', slug=slug)
        else:
            order = Order(
                user=user,
                phone=phone,
                total_paid=total_paid,
                ordered_date=ordered_date,
            )
            order.save()
            order_item = OrderApartment(item=item, quantity=2, saved_amount=saved_amount, order=order, final_price=final_price, user=request.user, ordered=False)
            order_item.save()
            return redirect('add_to_cart', slug=slug)
    else:
        return redirect('login')


@login_required(login_url='login')
def remove_from_cart(request, slug):
    item = get_object_or_404(Album, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    ap_order_qs = OrderApartment.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        ap_order = ap_order_qs
        if ap_order.filter(item__slug=item.slug).exists():
            order_item = OrderApartment.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_qs.delete()
            order_item.delete()
            return redirect('album', slug=slug)
        else:
            return redirect('album', slug=slug)
    else:
        return redirect('album', slug=slug)


@login_required(login_url='login')
def remove_from_cart2(request, slug):
    item = get_object_or_404(Album, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    ap_order_qs = OrderApartment.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        ap_order = ap_order_qs[0]
        if ap_order.filter(item__slug=item.slug).exists():
            order_item = OrderApartment.objects.filter(item=item, user=request.user, ordered=False)[0]
            return redirect('order-summary', slug=slug)
        else:
            return redirect('order-summary', slug=slug)
    else:
        return redirect('order-summary', slug=slug)


@login_required(login_url='login')
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Album, slug=slug)
    order_item, created = OrderApartment.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    ap_order_qs = OrderApartment.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        ap_order = ap_order_qs
        if OrderApartment.objects.filter(user=request.user, ordered=False, item__slug=item.slug).exists():
            order_item = OrderApartment.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity >= 4:
                order_item.quantity -= 1
                total_paid = order_item.item.real_price * order_item.quantity
                order = Order.objects.get(user=request.user)
                order.total_paid = total_paid
                order.save()
                order_item.save()
            else:
                pass
            return HttpResponseRedirect(
                '/<str:user>/my_order_details/{}'.format(order_item.order.id)
            )
        else:
            return HttpResponseRedirect(
                '/<str:user>/my_order_details/{}'.format(order_item.order.id)
            )
    else:
        return HttpResponseRedirect(
            '/<str:user>/my_order_details/{}'.format(order_item.order.id)
        )


@login_required(login_url='login')
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Album, slug=slug)
    order_item, created = OrderApartment.objects.get_or_create(item=item, user=request.user, ordered=False)
    ap_order_qs = OrderApartment.objects.filter(user=request.user, ordered=False)
    user = CustomUser.objects.get(user=request.user)
    rendom = Random_users.objects.get(admin=user)
    phone = rendom.phone
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_obj = Order.objects.get(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        ap_order = ap_order_qs
        if OrderApartment.objects.filter(user=request.user, ordered=False, item__slug=item.slug).exists():
            order_item.quantity += 1
            total_paid = order_item.item.real_price * order_item.quantity
            order = Order.objects.get(user=request.user)
            order.total_paid = total_paid
            order.save()
            order_item.save()
            return HttpResponseRedirect(
                '/<str:user>/my_order_details/{}'.format(order_item.order.id)
            )
        else:
            item_ord = OrderApartment.objects.create(user=request.user, item=item, quantity=1, order=order_obj)
            return HttpResponseRedirect(
                '/<str:user>/my_order_details/{}'.format(order_item.order.id)
            )
    else:
        total_paid = item.real_price * 1
        ordered_date = timezone.now()
        saved_amount = item.price - item.real_price
        final_price = item.real_price * 1
        order = Order.objects.create(user=request.user, total_paid=total_paid, ordered_date=ordered_date, phone=phone,
                                     ordered=False)
        order_ap = OrderApartment.objects.create(user=request.user, final_price=final_price, saved_amount=saved_amount, order=order,
                                  ordered=False, item=item, quantity=1)
        return HttpResponseRedirect(
            '/<str:user>/my_order_details/{}'.format(order_item.order.id)
        )

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "this coupon does not exist")
        return redirect('checkout_view')

class AddCouponView(View):
    def post(self, request, *args, **kwargs):
        form = CouponForm[request.POST or None]
        if form.is_valid():
            try:
                code = form.cleaned_data('code')
                order = Order.objects.filter(user=request.user, ordered=False)
                order.coupon = get_coupon(request, code)
                order.save()
                return redirect('checkout_view')
            except ObjectDoesNotExist:
                messages.info(request, "You do not have active order")
                return redirect('checkout_view')


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_request = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                return redirect('/')

            except ObjectDoesNotExist:
                return redirect('request-refund')


def signup(request):
    return render(request, "home_template/signup_template.html")

def logout(request):
    return render(request, "home_template/home.html")


def signup_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        if customer_form.is_valid():
            user = User(email=request.POST['email'], username=request.POST['username'],
                                  password=request.POST['password'], first_name=request.POST['first_name'],
                                  last_name=request.POST['last_name'])
            user.save()
            customer = CustomUser(user=user, user_type = 5)
            customer.save()
            random_user = Random_users(admin=customer, phone=request.POST['phone'])
            random_user.save()
            messages.success(request, "User Added Successfully!")
            return redirect('login')
    else:
        customer_form = AddCustomerForm()
        context = {
            'customer_form': customer_form,
        }
        return render(request, 'home_template/signup_template.html', context)


class EditOrderView(View):
    """View to edit order"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=kwargs['order_id'])
            form = OrderForm(instance=order)
            context = {
                'form': form,
                'order': order,
            }
            return render(request, 'home_template/edit_order.html', context)

        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=kwargs['order_id'])
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(
                    '/my_order_details/{}'.format(order.id)
                )
            context = {
                'form': form,
                'order': order,
            }
            return render(request, 'home_template/edit_order.html', context)

        else:
            return redirect('login')


class DeleteOrderView(View):
    """View to delete order"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=kwargs['order_id'])
            context = {
                'order': order,
            }
            return redirect('checkout_view')
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=kwargs['order_id'])
            order.delete()
            return redirect('my_orders')

        else:
            return redirect('login')


class EditOrderItemView(View):
    """View to edit order item"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_item = get_object_or_404(
                OrderApartment,
                id=kwargs['order_item_id']
            )
            # get product inventory
            product_inventory = get_object_or_404(
                Album,
                id=order_item.item.id
            )
            # get sale_price
            sale_price = product_inventory.real_price
            # origin quantity
            origin_quantity = order_item.quantity
            # multiply sale_price and origin quantity
            total_price = sale_price * origin_quantity
            form = OrderItemForm(instance=order_item)
            context = {
                'form': form,
                'order_item': order_item,
            }
            return render(request, 'home_template/edit_order_item.html', context)

        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_item = get_object_or_404(
                OrderApartment,
                id=kwargs['order_item_id']
            )
            # get product inventory
            product_inventory = get_object_or_404(
                Album,
                id=order_item.item.id
            )
            # get sale_price
            sale_price = product_inventory.real_price
            # origin quantity
            origin_quantity = order_item.quantity
            origin_spending = origin_quantity * sale_price
            # get quantity from form
            form_quantity = request.POST.get('quantity')
            # get updated spending
            new_spending = int(form_quantity) * sale_price
            # get the order
            order = order_item.order
            # get order total paid
            order_total_paid = order.total_paid
            new_total = order_total_paid - origin_spending + new_spending
            # update order total paid
            order.total_paid = new_total
            order.save()
            form = OrderItemForm(request.POST, instance=order_item)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(
                    '/my_order_details/{}'.format(order_item.order.id)
                )
            context = {
                'form': form,
                'order_item': order_item,
            }
            return render(request, 'home_template/edit_order_item.html', context)

        else:
            return redirect('login')


class DeleteOrderItemView(View):
    """View to delete order item"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_item = get_object_or_404(
                OrderApartment,
                id=kwargs['order_item_id']
            )
            context = {
                'order_item': order_item,
            }
            return render(
                request,
                'home_template/delete_order_item.html',
                context
            )

        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_item = get_object_or_404(
                OrderApartment,
                id=kwargs['order_item_id']
            )
            product_inventory = get_object_or_404(
                Album,
                id=order_item.item.id
            )
            # get sale_price
            sale_price = product_inventory.real_price
            # origin quantity
            origin_quantity = order_item.quantity
            origin_spending = origin_quantity * sale_price
            # get the order
            order = order_item.order
            # get order total paid
            order_total_paid = order.total_paid
            new_total = order_total_paid - origin_spending
            # update order total paid
            order.total_paid = new_total
            order.save()
            order_item.delete()
            return HttpResponseRedirect(
                '/my_order_details/{}'.format(order.id)
            )

        else:
            return redirect('login')


def AddOrderAJAXView(request, slug):
    """View for adding order AJAX."""
    if request.user.is_authenticated:
        item = get_object_or_404(
            Album, slug=slug
        )
        user = request.user
        rendom = Random_users.objects.get(admin__user=user)
        phone = rendom.phone
        order_item, created = OrderApartment.objects.get_or_create(item=item, user=request.user, ordered=False)
        ap_order_qs = OrderApartment.objects.filter(user=request.user, ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order_obj = Order.objects.get(user=request.user, ordered=False)
        if order_qs.exists():
            ap_order = ap_order_qs[0]
            if ap_order.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()

                return redirect('album', slug=slug)
            else:
                item_ord = OrderApartment.objects.create(user=request.user, item=item, quantity=1,
                                                             order=order_obj)
                return redirect('album', slug=slug)
        else:
            total_paid = item.real_price * 1
            ordered_date = timezone.now()
            saved_amount = item.price - item.real_price
            final_price = item.real_price * 1
            order = Order.objects.create(
                user=user,
                phone=phone,
                total_paid=total_paid,
                ordered_date=ordered_date,
            )
            item = OrderApartment.objects.create(
                user=user,
                order=order,
                saved_amount=saved_amount,
                final_price=final_price,
                item=item,
                quantity=1,
            )
            return redirect('album', slug=slug)
    else:
        return redirect('login')


class my_delete_orders(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            order = get_object_or_404(Order, id=kwargs['order_id'])
            orders = Order.objects.filter(user=user, ordered=False)
            order.delete()
            context = {
                "user": user,
                "orders": orders,
            }
            return render(request, 'home_template/user_orders.html', context)

        else:
            return redirect('login')


class my_delete_orders2(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            item = get_object_or_404(Album, slug=kwargs['slug'])
            user = request.user
            orders = Order.objects.filter(ordered=False, user=user)
            ap_order = OrderApartment.objects.get(ordered=False, item=item, user=user)
            order = ap_order.order
            ap_order.delete()
            order.delete()
            context = {
                "user": user,
                "orders": orders,
            }
            return render(request, 'home_template/product.html', context)

        else:
            return redirect('login')



