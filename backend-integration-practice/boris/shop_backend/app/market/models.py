from decimal import Decimal
from django.db import models
from account.models import UserProfile

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# ---------- Product ----------
class Product(TimeStampedModel):
    code = models.CharField(max_length=64, unique=True)
    name  = models.CharField(max_length=180)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True) # 可能會做filter，故設定索引
    category = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True, default="")
    is_active   = models.BooleanField(default=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active", "price"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=Decimal("0.00")), name="product_price_non_negative"),
        ]

    def __str__(self):
        return f"{self.name} ({self.product_code})"

# ---------- Cart & CartItem ----------
class Cart(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["profile", "created_at"])]

    def __str__(self):
        return f"Cart<{self.id}> for {self.profile_id}"

    @property
    def subtotal(self) -> Decimal:
        return sum(i.subtotal for i in self.items.all()) # 從CartItem算總金額

    @property
    def total_qty(self) -> int:
        return sum(i.qty for i in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="cart_items")
    qty = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cart", "product")
        indexes = [models.Index(fields=["cart"]), models.Index(fields=["product"])]
        constraints = [
            models.CheckConstraint(check=models.Q(qty__gte=1), name="cartitem_qty_gte_1"),
        ]

    def __str__(self):
        return f"{self.product.name} x {self.qty}"

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.qty

# ---------- Order & OrderItem ----------
class OrderStatus(models.TextChoices):
    PENDING   = "PENDING", "待付款"
    PAID      = "PAID", "已付款"
    CANCELED  = "CANCELED", "已取消"
    FULFILLED = "FULFILLED", "已完成"

class Order(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="orders")
    number = models.CharField(max_length=40, unique=True)
    status   = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), db_index=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [models.Index(fields=["status"]), models.Index(fields=["created_at"])]
        constraints = [
            models.CheckConstraint(check=models.Q(total_price__gte=Decimal("0.00")), name="order_totalprice_non_negative"),
        ]

    def __str__(self):
        return f"Order<{self.order_no}> - {self.status}"

    def recompute_total(self):
        self.total_price = sum(i.subtotal for i in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    qty = models.PositiveIntegerField()

    class Meta:
        indexes = [models.Index(fields=["order"]), models.Index(fields=["product"])]
        constraints = [
            models.CheckConstraint(check=models.Q(qty__gte=1), name="orderitem_qty_gte_1"),
        ]

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.qty

