# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as BS
from webdriver_manager.chrome import ChromeDriverManager
import pandas as PD

def scrape_info():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    # **NASA Mars News**

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse thru the HTML with Beautiful Soup
    soup = BS(html, 'html.parser')

    # Retrieve the latest news title
    News_Title = soup.find_all('div', class_ = 'content_title')
    Latest_News_Title = News_Title[0].text

    # Retrieve the paragraph for the latest news title
    Paragraph = soup.find_all('div', class_ = 'article_teaser_body')
    Latest_Paragraph = Paragraph[0].text

    # **JPL Mars Space Images - Featured Image**

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Use Splinter to find the image URL for the current Featured Mars Image
    Full_Image_Button = browser.links.find_by_partial_text('FULL IMAGE').click()

    # HTML Object
    html = browser.html

    # Parse thru the HTML with Beautiful Soup
    soup = BS(html, 'html.parser')

    # Retrieve the Full Size jpg Image URL
    image = soup.find('img', class_ = "fancybox-image")
    Featured_Image_Src = (image['src'])
    Featured_Image_URL = url + Featured_Image_Src

    # **Mars Facts**

    url = 'https://galaxyfacts-mars.com/'

    # Use PANDAS to scrape the Mars table on the above site
    tables = PD.read_html(url)[0]

    # Clean up DF and set index
    Mars_Data = tables
    Mars_Data.columns = ['Description', 'Mars', 'Earth']
    Mars_Data.set_index('Description', inplace = True)

    # Convert data to HTML table string and save to HTML file
    Mars_HTML_Data = Mars_Data.to_html()
    Mars_HTML_Data.replace('\n', '')
    Mars_HTML_Data = Mars_Data.to_html(classes = 'table table-striped')

    # **Mars Hemispheres**

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse thru the HTML with Beautiful Soup
    soup = BS(html, 'html.parser')

    # Identify list
    H_List = soup.find_all('div', class_= "item")

    url = "https://marshemispheres.com/"

    hemisphere_image_urls = []

    for item in H_List:
    
        # Retrieve Title for Image and Image details
        Title = item.find("h3").text
        Image = item.find("a", class_= "itemLink product-item")["href"]
    
        # Access each Hemisphere link
        browser.visit(url + Image)
    
        # HTML Object
        html = browser.html
    
        # Parse thru the HTML with Beautiful Soup
        soup = BS(html, "html.parser")
    
        # Retrieve the Full Size jpg Image URL
        Image_URL = url + soup.find("img", class_= "wide-image")["src"]
    
        # Append Data
        hemisphere_image_urls.append({"title" : Title, "img_url" : Image_URL})

    # Store Data in Dictionary
    mars_data = {
        "Latest_News_Title": Latest_News_Title,
        "Latest_Paragraph": Latest_Paragraph,
        "Featured_Image_URL": Featured_Image_URL,
        "Mars_HTML_Data": Mars_HTML_Data,
        "Hemisphere_Image_URLs": hemisphere_image_urls
    }

    # Close the browser
    browser.quit()

    # Return Results
    return mars_data

data = scrape_info()
print(data)

