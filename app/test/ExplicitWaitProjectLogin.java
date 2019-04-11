package System_Testing;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.NoAlertPresentException;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class ExplicitWaitProjectLogin {
	
	static String myUserName = "member";
	static String myPassword = "Password1";
	
	public static void main(String[] args) throws InterruptedException {		

		System.setProperty("webdriver.chrome.driver","/Users/ih/SUTD/ISTD/Term 5/50.003 ESC/selenium-java-3.141.59/chromedriver");
		WebDriver driver = new ChromeDriver();
		WebDriverWait alertWait = new WebDriverWait(driver, 5);
		
		driver.get("http://127.0.0.1:5000/");
		HandleAlert(driver, alertWait);

		// get all the links
		java.util.List<WebElement> links = driver.findElements(By.tagName("a"));
		System.out.println(links.size());
		
		// get the user name field of the account page
		WebElement username = driver.findElement(By.name("email"));
		
		// send my user name to fill up the box
		username.sendKeys(myUserName);
		username.sendKeys(Keys.TAB);
		
		//explicitly wait until the password field is present in the page
		try {
			WebDriverWait wait = new WebDriverWait(driver, 2);
			// wait only until the password element becomes visible
			wait.until(ExpectedConditions.elementToBeClickable(By.name("password")));		
			wait.until(ExpectedConditions.alertIsPresent());
			// now locate the password field in the current page
			WebElement password = driver.findElement(By.name("password"));		
			// send password 
			password.sendKeys(myPassword);
			// login and :)
			WebElement signInButton = driver.findElement(By.id("sign_in"));		
			signInButton.click();
		} catch (Exception NoSuchElementException) {
			System.out.println("login name or password invalid");
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
	}
}