from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By


driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(
), 'geckodriver.exe'), firefox_binary='C:\\Program Files\\Mozilla Firefox\\firefox.exe')

driver.get(
    "https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/")


time.sleep(3)

# ul id=/undergraduate-calendar/course-descriptions/ > li > a
urls = driver.find_elements(
    By.XPATH, "//ul[@id='/undergraduate-calendar/course-descriptions/']/li/a")

urls = [url.get_attribute('href') for url in urls]


# Go to each url and execute the following javascript:

"""let courses = document.querySelectorAll(".courseblock");

// Assuming 'courses' is an array that contains each course element
let coursesArray = [];

for (let course of courses) {
    // Extract properties by targeting specific indexes
    let properties = Array.from(course.children);

    // Extract data into an object
    let courseData = {
        title: properties[0] ? properties[0].innerText : null,
        description: properties[1] ? properties[1].innerText : null,
        offerings: properties[2] ? properties[2].innerText : null,
        prerequisites: properties[4] ? properties[4].innerText : null,
        coRequisites: properties[5] ? properties[5].innerText : null,
        equates: properties[6] ? properties[6].innerText : null,
        restrictions: properties[7] ? properties[7].innerText : null,
        department: properties[8] ? properties[8].innerText : null,
        locations: properties[9] ? properties[9].innerText : null,
    };

    // Add the courseData object to the coursesArray
    coursesArray.push(courseData);
}

// Convert coursesArray to JSON
let coursesJSON = JSON.stringify(coursesArray);

// Output the JSON
console.log(coursesJSON);"""


for url in urls:
    driver.get(url)
    # Too lazy to copy over the wait for load function from my other project so wait instead
    time.sleep(1)
    output = driver.execute_script("""let courses = document.querySelectorAll(".courseblock");

    // Assuming 'courses' is an array that contains each course element
    let coursesArray = [];

    for (let course of courses) {
        // Extract properties by targeting specific indexes
        let properties = Array.from(course.children);

        // Extract data into an object
        let courseData = {
            title: properties[0] ? properties[0].innerText : null,
            description: properties[1] ? properties[1].innerText : null,
            offerings: properties[2] ? properties[2].innerText : null,
            prerequisites: properties[4] ? properties[4].innerText : null,
            coRequisites: properties[5] ? properties[5].innerText : null,
            equates: properties[6] ? properties[6].innerText : null,
            restrictions: properties[7] ? properties[7].innerText : null,
            department: properties[8] ? properties[8].innerText : null,
            locations: properties[9] ? properties[9].innerText : null,
        };

        // Add the courseData object to the coursesArray
        coursesArray.push(courseData);
    }

    // Convert coursesArray to JSON
    let coursesJSON = JSON.stringify(coursesArray);

    // Output the JSON
    return coursesJSON;""")

    with open('data.txt', 'a') as f:
        f.write(output)


driver.close()
