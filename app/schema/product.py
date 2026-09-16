from pydantic import BaseModel, Field, AnyUrl, field_validator, model_validator, computed_field, EmailStr
from typing import Annotated, Literal, Optional, List
from uuid import UUID
from datetime import datetime


class Product(BaseModel):
    id: UUID
    sku: Annotated[
        str, 
        Field(min_length=6, 
        max_length=50, 
        title="SKU", 
        description="Stock Keeping Unit")
    ]    
    name:  Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="Product Name",
            description="Readable product name (3-80 chars).",
            examples=["Xiaomi Model Pro", "Apple Model X"],
        ),
    ]

    description: Annotated[
        str,
        Field(max_length=200, description="Short product description"),
    ]

    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="Category like mobiles/laptops/electronics/accessories",
            examples=["mobiles", "laptops"],
        ),
    ]

    brand: Annotated[
        str,
        Field(min_length=2, max_length=40, examples=["Xiaomi", "Apple"]),
    ]

    price: Annotated[float, Field(gt=0, strict=True, description="Base price (INR)")]
    currency: Literal["INR"] = "INR"

    discount_percent: Annotated[
        int,
        Field(ge=0, le=90, description="Discount in percent (0-90)"),
    ] = 0

    stock: Annotated[int, Field(ge=0, description="Available stock (>=0)")]
    is_active: Annotated[bool, Field(description="Is product active?")]

    rating: Annotated[
        float,
        Field(ge=0, le=5, strict=True, description="Rating out of 5"),
    ]

    tags: Annotated[
        Optional[List[str]],
        Field(default=None, max_length=10, description="Up to 10 tags"),
    ]
    image_urls: Annotated[
        List[AnyUrl],
        Field(max_length=1, description="At least 1 image url"),
    ]

    class Dimemsion(BaseModel):
        length: Annotated[float, Field(gt=0, strict=True, description="Length")]
        width: Annotated[float, Field(gt=0, strict=True, description="Width")]
        height: Annotated[float, Field(gt=0, strict=True, description="Height")]
        weight: Annotated[float, Field(gt=0, strict=True, description="Weight")]

    dimensions: Dimemsion
    
    class Seller(BaseModel):
        id : UUID
        name: Annotated[
            str,
            Field(min_length=2, max_length=40, examples=["Xiaomi", "Apple"]),
        ] 

        email: EmailStr
        website_url: AnyUrl

        @field_validator("email", mode="after") 
        @classmethod
        def validate_email_domain(cls, value: EmailStr):
            allowed_domains = ["mistore.in", "amazon.in", "hpworld.in", 
            "redmi.in", "po.in", "realme.in", "samsung.in", "apple.in", 
            "lenovo.in", "dell.in", "lg.in", "sony.in", "panasonic.in",
            "flipkart.com", "snapdeal.com", "myntra.com", "ajio.com",
            "nykka.com", "purplle.com", "nykaa.com", "cult.fit"]

            _, domain = value.split("@")
            if domain not in allowed_domains:
                raise ValueError("Email domain is not allowed")
            return value 

    seller: Seller
    created_at: datetime
    dimension: Dimemsion

    @field_validator('sku', mode="after")
    @classmethod
    def validate_sku_formate(cls, value:str):
        if "-" not in value:
            raise ValueError("SKU must contain at least one hyphen")

        last = value.split("-")[-1]
        if not last.isdigit() or len(last) != 3:
            raise ValueError("Last part of SKU must be a 3-digit number")
        
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model:'Product'):
        if model.stock == 0 and model.is_active == True:
            raise ValueError("Product cannot be active if stock is 0")

        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discount cannot be applied to a product with no rating")

    @computed_field
    @property
    def final_price(self)-> float:
      return round(self.price * (1 - (self.discount_percent / 100)), 2) 

        
            

