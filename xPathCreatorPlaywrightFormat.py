
# for Xpath only
explainerLineOne = '\nUsing Dev Tools in your browser, copy the Xpath for the element you want to interact with\n'
explainerLineTwo = "it will have this template form, //div[@id='element_id']"
explainerLineThree = "OR you can copy this entire line and paste it into your Playwright file\n"

print(explainerLineOne)
print(explainerLineTwo)

unformattedXpath = input("\nPaste it here: ")

pwXpath = (f"\nPaste this line into your playwright script, including the quote marks:\n\n'xpath = {unformattedXpath}'\n")

pwXpathFullFormat = (f"page.locator('xpath = {unformattedXpath}')\n")


print(pwXpath)

print(explainerLineThree)

print(pwXpathFullFormat)
