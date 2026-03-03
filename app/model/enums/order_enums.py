from enum import Enum


class OrderType(str, Enum):
    dry_cleaning = "dry_cleaning"
    wash_and_fold = "wash_and_fold"
    steam_press_ironing = "steam_press_ironing"
    stain_removal = "stain_removal"
    suede_leather = "suede_leather"


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    picked_up = "picked_up"
    in_cleaning = "in_cleaning"
    in_ironing = "in_ironing"
    quality_check = "quality_check"
    ready_for_delivery = "ready_for_delivery"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"
