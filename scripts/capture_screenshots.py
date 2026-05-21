"""ถ่าย screenshot หน้าเว็บสำหรับ README (ต้องรัน runserver ก่อน)."""
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000"
OUT = Path(__file__).resolve().parent.parent / "docs" / "screenshots"


def shot(page, name: str, path: str, *, full_page: bool = True) -> None:
    page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=60000)
    page.screenshot(path=OUT / f"{name}.png", full_page=full_page)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        for name, path in [
            ("01-home", "/"),
            ("02-products", "/products/"),
            ("03-product-detail", "/products/1/"),
            ("04-register", "/register/"),
            ("05-login", "/login/"),
        ]:
            shot(page, name, path)

        page.goto(f"{BASE}/login/", wait_until="networkidle")
        page.fill('input[name="username"]', "somchai")
        page.fill('input[name="password"]', "Member2025!")
        page.locator('button[type="submit"]').click()
        page.wait_for_load_state("networkidle")
        shot(page, "06-profile", "/profile/")
        shot(page, "07-cart", "/cart/")

        page.goto(f"{BASE}/manage/login/", wait_until="networkidle")
        page.fill('input[name="username"]', "viperadmin")
        page.fill('input[name="password"]', "ViperSport2025!")
        page.locator('button[type="submit"]').click()
        page.wait_for_load_state("networkidle")
        shot(page, "08-admin-dashboard", "/manage/")
        shot(page, "09-admin-product-form", "/manage/products/add/")

        browser.close()
    print(f"Saved screenshots to {OUT}")


if __name__ == "__main__":
    main()
