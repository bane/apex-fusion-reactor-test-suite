from time import sleep
from datetime import datetime
from toolbox.chrome import Chrome
from toolbox.utils import retry


class MetaMask:
    def __init__(
            self,
            driver: Chrome,
            sign_key: str,
            subnetwork: str,
            token_name: str
    ) -> None:

        self.__url: str = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html'
        self.__add_network_url: str = f'{self.__url}#settings/networks/add-network'
        self.__driver: Chrome = driver
        self.__sign_key: str = sign_key
        self.__subnetwork: str = subnetwork
        self.__token_name: str = token_name
        self.__receive_address: str = ""
        self.__opened_tabs: list[str] = self.__driver.window_handles

        self.__driver.switch_to.window(self.__driver.get_init_tab())

    @retry()
    def __agree_terms(self) -> None:
        self.__driver.find_element_by_xpath(
            '//*[@id="onboarding__terms-checkbox"]'
        ).click()

    @retry()
    def __import_wallet(self) -> None:
        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[3]/button'
        ).click()

    @retry()
    def __no_improve(self) -> None:
        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button[1]'
        ).click()

    @retry()
    def __recover_phrase(self, recovery_phrase: str) -> None:
        phrase = recovery_phrase.split()

        for i in range(len(phrase)):

            self.__driver.find_element_by_xpath(
                f'//*[@id="import-srp__srp-word-{i}"]'
            ).send_keys(phrase[i])

    @retry()
    def __confirm_phrase(self) -> None:
        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button'
        ).click()

    @retry()
    def __set_sign_key(self) -> None:
        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input'
        ).send_keys(self.__sign_key)

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input'
        ).send_keys(self.__sign_key)

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input'
        ).click()

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'
        ).click()

    @retry()
    def __unlock(self) -> None:
        self.__driver.find_element_by_xpath(
            '//*[@id="password"]'
        ).send_keys(self.__sign_key)

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[3]/div/div/div/div/button'
        ).click()

    @retry()
    def __got_it(self) -> None:
        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
        ).click()

    @retry()
    def __finish(self) -> None:
        bnt = self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
        )

        for i in range(2):

            bnt.click()
            sleep(1)

    @retry()
    def __set_receive_address(self) -> None:
        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div[3]/div/div/button'
        ).click()

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]'
        ).click()

        self.__receive_address = self.__driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div/section/div/div/div[2]/p'
        ).text

    def get_receive_address(self) -> str:
        return self.__receive_address

    def get_subnetwork(self) -> str:
        return self.__subnetwork

    def get_web_app_identifier(self) -> str:
        return self.__subnetwork

    def get_token_name(self) -> str:
        return self.__token_name

    def recover(self, recovery_phrase: str) -> None:
        print(f"{datetime.now()} Start recovering {self.__subnetwork} wallet")

        self.__driver.get(self.__url)
        self.__agree_terms()
        self.__import_wallet()
        self.__no_improve()
        self.__recover_phrase(recovery_phrase)
        self.__confirm_phrase()
        self.__set_sign_key()
        self.__driver.get(self.__url)
        self.__unlock()
        self.__got_it()
        self.__finish()

        print(f"{datetime.now()} {self.__subnetwork.capitalize()} wallet recovered successfully")

    def toggle(self) -> None:
        pass

    @retry()
    def add_network(self, name: str, rpc_url: str, chain_id: str, currency_symbol: str) -> None:
        self.__driver.get(self.__add_network_url)

        sleep(5)

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/input'
        ).send_keys(name)

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/label/input'
        ).send_keys(rpc_url)

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div/input'
        ).send_keys(chain_id)

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[4]/div/input'
        ).send_keys(currency_symbol)

        self.__driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/button[2]'
        ).click()

        sleep(1)

        self.__driver.find_element_by_xpath(
            '//*[@id="popover-content"]/div/div/section/div[2]/div/button[1]'
        ).click()

        print(f"{datetime.now()} {name} network successfully added")

        sleep(1)

        self.__driver.get(self.__url)
        self.__set_receive_address()
        self.__driver.get(self.__url)

        print(f'{datetime.now()} {self.__subnetwork.capitalize()} address: {self.__receive_address}')

    @retry()
    def grant_access(self) -> None:
        popup = list(set(self.__driver.window_handles) - set(self.__opened_tabs))[0]

        self.__driver.switch_to.window(popup)

        for i in range(2):

            self.__driver.find_element_by_xpath(
                '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]'
            ).click()

            sleep(1)

        # wait access to be granted
        sleep(5)

        self.__driver.switch_to.window(self.__driver.get_init_tab())
