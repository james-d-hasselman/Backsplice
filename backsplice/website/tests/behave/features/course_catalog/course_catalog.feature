Feature: View the course catalog

    Scenario: View catalog with courses
        When there are courses in the catalog
        And the user navigates to the url "/course_catalog"
        Then the courses are displayed

    Scenario: View catalog without courses
        When there are no courses in the catalog
        And the user navigates to the url "/course_catalog"
        Then a message is displayed indicating "The Course Catalog does not contain any courses."

    Scenario: Navigate to the edit page
        When the user is on the "/course_catalog" page
        And the user clicks "Edit"
        Then the course catalog edit page is displayed

    Scenario: Navigate to the import page
        When the user is on the "/course_catalog" page 
        And the user clicks "Import"
        Then the import courses page is displayed
