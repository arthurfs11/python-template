import asyncio
from time import sleep

from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import HcaptchaProxylessRequest, RecaptchaV2ProxylessRequest,RecaptchaV3ProxylessRequest,RecaptchaV2EnterpriseProxylessRequest
from loguru import logger

from app.__main__ import Captcha


class CapMonster:
    def __init__(self,token):
        self._cap_monster_client = CapMonsterClient(options=ClientOptions(api_key=token))

    async def solve(self, req):
        return await self._cap_monster_client.solve_captcha(req)

    def solve_recaptcha(self, web_site_url, site_key,v="v2",tries=3):
        if v =="v2":
            req = RecaptchaV2EnterpriseProxylessRequest(websiteUrl=web_site_url, websiteKey=site_key)
        else:
            req = RecaptchaV3ProxylessRequest(websiteUrl=web_site_url, websiteKey=site_key,min_score=0.9,pageAction="grecaptcha")

        try:
            logger.debug("Solving recaptcha")
            responses = asyncio.run(self.solve(req))
            logger.debug("Recaptcha solved")
        except Exception as e:
            if tries == 0:
                logger.critical(f"Error solving captcha:{str(e)}")
                raise Exception(f"Error solving captcha:{str(e)}")
            sleep(2)
            return self.solve_recaptcha(web_site_url, site_key,v=v, tries=tries - 1)

        return responses['gRecaptchaResponse']

    def solve_hcaptcha(self, web_site_url, site_key, tries=3):
        try:
            logger.info("Solving hcaptcha")
            req = HcaptchaProxylessRequest(
                websiteUrl=web_site_url,
                websiteKey=site_key,
                isInvisible=True,
            )
            response = asyncio.run(self.solve(req))
            logger.info("Hcaptcha solved")

            if response.get("errorId"):
                logger.error(f"Error ao resolver o recaptcha: {response.get('errorDescription')}")
                raise Exception(f"Error ao resolver o recaptcha: {response.get('errorDescription')}")
            return response.get("gRecaptchaResponse")
        except Exception as e:
            if tries == 0:
                logger.error(f"Error solving captcha:{str(e)}")
                raise Exception(f"Error solving captcha:{str(e)}")
            sleep(2)
            return self.solve_hcaptcha(web_site_url, site_key, tries=tries - 1)