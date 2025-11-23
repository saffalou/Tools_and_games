
# this is an upgrade to xPathCreatorPLaywrightFormat.py
# it will allow you to create locators for different types of elements
while True:
    whichLocator = input("\nWhich locator do you want to use? ((I)d, (C)lass,(X)path, C(S)S): ")

    if whichLocator.upper() == "I":
        elementId = input("Enter the element ID: ")
        locator = f"await page.locator('#{elementId}')"
        print(f'\nCopy this locator and add to your Playwright test file:\n{locator}\n')

    elif whichLocator.upper() == "C":
        elementClass = input("Enter the element class: ")
        locator = f"await page.locator('.{elementClass}')"
        print(f'\nCopy this locator and add to your Playwright test file:\n{locator}\n')

    elif whichLocator.upper() == "X":
        xpath = input("Enter the XPath: ")
        locator = f"await page.locator('xpath={xpath}')"
        print(f'\nCopy this locator and add to your Playwright test file:\n{locator}\n')

    elif whichLocator.upper() == "S":
        cssSelector = input("Enter the CSS selector: ")
        locator = f"await page.locator('css={cssSelector}')"
        print(f'\nCopy this locator and add to your Playwright test file:\n{locator}\n')

    else:
        print("\nInvalid locator type. Please try again.")
        continue

    again_prompt = input("\nDo you want to create another locator? (Y/N): ")
    if again_prompt.upper() == "N":
        break
    elif again_prompt.upper() != "Y":
        print("\nInvalid input. Please try again.")