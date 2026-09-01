import asyncio
import time
import httpx
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
api_llm_url = os.getenv("API_LLM_URL")

payload = {
    "model": "qwen3.5:4b-mlx",
    "prompt": "สวัสดี แนะนำตัวเองสั้นๆ หน่อย",
    "stream": False
}

headers = {
    "Authorization": f"Bearer {api_key}",
}

async def call_api_async(
    url: str,
    payload: dict,
    headers: dict,
    timeout: float = 300.0
) -> dict:

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers,
            timeout=timeout
        )

        response.raise_for_status()

        return response.json()





async def main():

    print("Calling Ollama...")
    print("URL:", api_llm_url)
    print("Model:", payload["model"])

    i = 0

    while i < 3:
        try:

            ollama_result = await call_api_async(
                api_llm_url,
                payload,
                headers
            )

            result = {
                "answer": ollama_result["response"],
                "model": ollama_result["model"],
                "usage": {
                    "prompt_tokens": ollama_result.get("prompt_eval_count", 0),
                    "completion_tokens": ollama_result.get("eval_count", 0),
                    "total_duration": ollama_result.get("total_duration", 0)
                }
            }

            print(result)

        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code

            if status_code == 401:
                print("API key ไม่ถูกต้องหรือหมดอายุ")
                break
            elif status_code == 429:
                print("โดน rate limit — retry")
            elif status_code >= 500:
                print("Server error — retry")
            else:
                print(f"HTTP Error: {status_code}")
                break

        except httpx.TimeoutException:
            print("Request timeout — retry")

        i += 1


# asyncio.run(main())

async def call_multiple_prompts(
    url: str,
    prompts: list[str],
    headers: dict
) -> list[dict]:

    start = time.perf_counter()

    tasks = [
        call_api_async(
            url,
            {
                "model": "qwen3.5:4b-mlx",
                "prompt": prompt,
                "stream": False
            },
            headers
        )
        for prompt in prompts
    ]

    results = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start

    print(f"Total time: {elapsed:.2f} seconds")

    return results


async def main2():
    prompts = [
        "เล่าเรื่องสั้นๆ",
        "แปลคำว่า hello",
        "1+1 เท่ากับเท่าไหร่"
    ]

    ollama_results = await call_multiple_prompts(
        api_llm_url,
        prompts,
        headers
    )

    for ollama_result in ollama_results:
        result = {
            "answer": ollama_result["response"],
            "model": ollama_result["model"],
            "usage": {
                "prompt_tokens": ollama_result.get("prompt_eval_count", 0),
                "completion_tokens": ollama_result.get("eval_count", 0),
                "total_duration": ollama_result.get("total_duration", 0)
            }
        }
        print(result["answer"])


asyncio.run(main2())
