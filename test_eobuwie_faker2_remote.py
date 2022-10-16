import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.relative_locator import locate_with
from time import sleep
from faker import Faker

GRID_HUB_URL = "http://127.0.0.1/wd/hub"

# DANE TESTOWE
haslo = "dfsdffe565675&&&"


class RejestracjaNowegoUzytkownika(unittest.TestCase):
    def setUp(self):
        # WARUNKI WSTĘPNE
        # 1. Otwarta strona główna
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.EDGE)
        self.driver.maximize_window()
        self.driver.get("https://www.eobuwie.com.pl/")
        # (2. Użytkownik niezalogowany)
        # Zamknij alert o ciasteczkach
        self.driver.find_element(By.CLASS_NAME, "e-button--type-primary.e-button--color-brand.e-consents-alert__button.e-button").click()
        self.fake = Faker("pl_PL")
    def testBrakPodaniaImienia(self):
        # Warunki Testowe
        haslo = "AlaMaKota123."
        sleep(10)
        # 1. Kliknij „Zarejestruj”
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Zarejestruj").click()
        # 2. Wpisz nazwisko
        nazwisko = self.driver.find_element(By.ID, "lastname")
        nazwisko.send_keys(self.fake.last_name())
        # 3. Wpisz adres email
        email = self.driver.find_element(By.ID, "email_address")
        email.send_keys("nowak72@hotmail.com")
        # 4. Wpisz hasło (co najmniej 6 znaków)
        haslo_wprowadzenie = self.driver.find_element(By.ID, "password")
        haslo_wprowadzenie.send_keys(haslo)
        # 5. Wpisz ponownie hasło
        haslo_powtórzenie = self.driver.find_element(By.ID, "confirmation")
        haslo_powtórzenie.send_keys(haslo)

        # 6. Zaznacz akceptację regulaminu
        akceptacja_regulaminu = self.driver.find_element(By.XPATH,"/html/body/div[3]/div/div/form/div[7]/label")
        akceptacja_regulaminu.click()

        # 7. Kliknij "Załóż nowe konto"
        załóż_konto = self.driver.find_element(By.ID, "create-account")
        załóż_konto.click()


        ### OCZEKIWANY REZULTAT ###
        # Użytkownik otrzymuje informację "To pole jest wymagane" pod imieniem.
        # 1. Szukam pola "imię".
        imie = self.driver.find_element(By.ID, "firstname")
        # 2. Szukam spana obok pola "imię" (nad nazwiskiem).
        error_span = self.driver.find_element(locate_with(By.XPATH,'//span[@class="form-error"]').near(imie))
        error_span2 = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').above(nazwisko))
        # Sprawdzam czy obie metody wskazują ten sam element
        print(error_span)
        print(error_span2)
        self.assertEqual(error_span.id, error_span2.id)

        # 3. Sprawdzam, czy jest tylko jeden taki span.
        errory = self.driver.find_elements(By.XPATH,'//span[@class="form-error"]')
        liczba_errorow = len(errory)
        self.assertEqual(liczba_errorow, 1)
        # 4. Sprawdzam, czy treść tego spana brzmi "To pole jest wymagane"
        komunikat_błędu = "To pole jest wymagane"
        self.assertEqual(error_span.text, komunikat_błędu)


        pass


    def tearDown(self):
        # Zakończenie testu
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()