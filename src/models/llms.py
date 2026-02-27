import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def load_llm(model_name):
    """Load Large Language Model.
    Args:
        model_name (str): Tên mô hình cần tải
    Raise:
        ValueError: Nếu tên mô hình không hợp lệ
    Return:
        Khởi tạo của mô hình tương ứng
    """
    if model_name == "gpt-3.5-turbo":
        return ChatOpenAI(
            model=model_name,
            temperature=0.0,
            max_tokens=1000, # Đổi thành max_tokens cho tương thích ngược tốt hơn
        )
    elif model_name == "gpt-4":
        return ChatOpenAI(
            model=model_name,
            temperature=0.0,
            max_tokens=1000,
        )
    elif model_name == "gemini-2.5-flash":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0,
            max_tokens=1000, # Đổi thành max_tokens cho tương thích ngược tốt hơn
        )
    else:
        # Cập nhật lại câu thông báo lỗi cho khớp với if-else
        raise ValueError(
            "Unknown model. Please choose from ['gpt-3.5-turbo','gpt-4','gemini-pro']"
        )