import httpx

async def get_faq():
    url = 'http://127.0.0.1:8000/faq_get_bot/'

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        if res.status_code == 200:
            response = res.json()
            return response

async def get_faq_children(id):
    url = f'http://127.0.0.1:8000/get_faq_children/{id}/'

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        if res.status_code == 200:
            response = res.json()
            return response

async def get_faq_byId(id):
    url = f'http://127.0.0.1:8000/get_faq_byId/{id}/'

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        if res.status_code == 200:
            response = res.json()
            print(response)
            return response