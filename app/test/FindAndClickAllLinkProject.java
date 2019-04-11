package System_Testing;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.UnhandledAlertException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.awt.AWTException;
import java.awt.event.KeyEvent;

import org.openqa.selenium.Alert;
import org.openqa.selenium.NoAlertPresentException;

public class FindAndClickAllLinkProject {
		
	public static void main(String[] args) throws InterruptedException, AWTException {		
		System.setProperty("webdriver.chrome.driver","/Users/ih/SUTD/ISTD/Term 5/50.003 ESC/selenium-java-3.141.59/chromedriver");
		WebDriver driver = new ChromeDriver();
		WebDriverWait wait = new WebDriverWait(driver, 5);

		driver.get("http://127.0.0.1:5000/");
		HandleAlert(driver, wait);

		//driver.get("https://www.google.com.sg");
		
		// get all the links
		java.util.List<WebElement> links = driver.findElements(By.tagName("a"));
		System.out.println(links.size());

		// print all the links
		for (int i = 0; i < links.size(); i=i+1) {
			System.out.println(i + " " + links.get(i).getText());
			System.out.println(i + " " + links.get(i).getAttribute("href"));
		}

		// maximize the browser window
		driver.manage().window().maximize();
		
		
		// click all links in a web page
		for(int i = 0; i < links.size(); i++)
		{
			System.out.println("*** Navigating to" + " " + links.get(i).getAttribute("href"));
			if (links.get(i).getAttribute("href") == null)
				continue;
			boolean staleElementLoaded = true;
			while(staleElementLoaded) {
				try {
					driver.navigate().to(links.get(i).getAttribute("href"));
					HandleAlert(driver, wait);
					Thread.sleep(3000);
					driver.navigate().back();
					links = driver.findElements(By.tagName("a"));
					System.out.println("*** Navigated to" + " " + links.get(i).getAttribute("href"));
					staleElementLoaded = false;
				} catch (StaleElementReferenceException e) {
					staleElementLoaded = true;
					}
				}
			}

		}
	
	public static void HandleAlert(WebDriver driver, WebDriverWait wait) {
	    if (wait == null) {
	        wait = new WebDriverWait(driver, 5);
	    }else {
			try{ 
			//wait.until(ExpectedConditions.alertIsPresent());
			Alert alert = driver.switchTo().alert();
			String alertMessage= alert.getText();	
			System.out.println("Pop-up message: " + alertMessage);
	        alert.accept();
			} catch (NoAlertPresentException e) {
				//e.printStackTrace();
			}
	    }
//		try {
//			wait.until(ExpectedConditions.alertIsPresent());
//
//		} catch (UnhandledAlertException f) {
//		    try {
//		        Alert alert = driver.switchTo().alert();
//		        String alertText = alert.getText();
//		        System.out.println("Alert data: " + alertText);
//		        alert.accept();
//		    } catch (NoAlertPresentException e) {
//		        e.printStackTrace();
//		    }
//		}
	}
}