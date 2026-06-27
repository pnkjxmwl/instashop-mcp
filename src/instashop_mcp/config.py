import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    ig_user_id: str
    ig_access_token:str
    ig_api_version:str

    razorpay_key_id:str
    razorpay_key_secret:str

    webhook_verify_token:str
    callback_url:str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            ig_user_id= os.environ["IG_USER_ID"],
            ig_access_token=os.environ["IG_ACCESS_TOKEN"],
            ig_api_version=os.environ["IG_API_VERSION"],
            razorpay_key_id=os.environ["RAZORPAY_KEY_ID"],
            razorpay_key_secret=os.environ["RAZORPAY_KEY_SECRET"],
            webhook_verify_token=os.getenv("WEBHOOK_VERIFY_TOKEN", ""),
            callback_url=os.getenv("RAZORPAY_CALLBACK_URL", ""),
        )

