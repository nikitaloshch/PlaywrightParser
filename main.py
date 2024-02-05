import asyncio
from playwright.async_api import async_playwright
from openpyxl import Workbook


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            await page.goto('https://www.python.org/downloads/', timeout=60000)
            print("Страница успешно загружена!")

            # Ожидаем видимости элемента
            await page.wait_for_selector('#content > div > section > div.row.download-list-widget > ol')

            # Извлекаем данные из таблицы с использованием page.evaluate
            data = await page.evaluate('''
                () => {
                    const items = document.querySelectorAll('#content > div > section > div.row.download-list-widget > ol > li');
                    return Array.from(items, item => {
                        const release_version = item.querySelector('.release-number a')?.textContent;
                        const release_date = item.querySelector('.release-date')?.textContent;
                        const release_download = item.querySelector('.release-download a')?.href;
                        const release_notes = item.querySelector('.release-enhancements a')?.href;

                        return [release_version, release_date, release_download, release_notes];
                    });
                }
            ''')

            # Записываем данные в Excel без использования pandas
            wb = Workbook()
            ws = wb.active
            ws.append(['Release version', 'Release date', 'Download', 'Release Notes'])
            for row in data:
                ws.append(row)

            # Сохраняем Excel файл
            wb.save('python_releases.xlsx')
            print("Данные успешно сохранены в python_releases.xlsx")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        await browser.close()

asyncio.run(main())
