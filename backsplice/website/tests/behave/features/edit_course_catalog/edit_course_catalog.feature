Feature: Edit Course Catalog

    Scenario: Navigate to the edit page with courses in the catalog
        When there are courses in the course catalog
        And the user navigates to the "/course_catalog/edit" page
        Then the courses are displayed one course per line with a text box containing the name of the course 
        And a textbox containing the period

    Scenario: Navigate to the edit page with no courses in the catalog
        When there are no courses in the course catalog
        And the user navigates to the "/course_catalog/edit" page
        Then a message is displayed indicating "The Course Catalog does not contain any courses."

    Scenario: Add course without providing course name
        When the user is on the "/course_catalog/edit" page
        And the user clicks "Add" without providing a course name
        Then an error message is displayed that says "Course name is required."

    Scenario: Add course without providing period
        When the user is on the "/course_catalog/edit" page
        And the user clicks "Add" without providing a period
        Then an error message is displayed that says "Period is required."

    Scenario: Save courses with one or more blank course names present 
        When there are courses in the course catalog
        And the user is on the "/course_catalog/edit" page
        And the course name of any course in the course catalog is made blank 
        And the user clicks "Save"
        Then the "/course_catalog/edit" page is displayed again with the previous course name restored
        And an error message is displayed that says "Course name cannot be blank."

    Scenario: Save courses with one or more blank periods
        When there are courses in the course catalog
        And the user is on the "/course_catalog/edit" page
        And the period of any course in the course catalog is made blank
        And the user clicks "Save"
        Then the "/course_catalog/edit" page is displayed again with the previous period restored 
        And an error message is displayed that says "Period cannot be blank."

    Scenario: Add course that already exists in the catalog
        When there are courses in the course catalog
        And the user is on the "/course_catalog/edit" page
        And the provided course name and period name match those of an existing course in the course catalog
        And the user clicks "Add"
        Then an error message is displayed that says "Course already present in the course catalog"

    Scenario: Save non-unique courses
        When there are courses in the course catalog
        And the user is on the "/course_catalog/edit" page
        And two or more courses in the course catalog have matching names and periods 
        And the user clicks "Save"
        Then the "/course_catalog/edit" page is displayed again with the offending change(s) reverted 
        And an error message is displayed that says "Courses must be unique."

    Scenario: Add new course to the catalog
        When the user is on the "/course_catalog/edit" page
        And the user has provided a valid course name and period 
        And the user clicks "Add"
        Then the "/course_catalog/edit" page is displayed again with the new course included in the course catalog section

    Scenario: Save changes to existing courses
        When there are courses in the course catalog
        And the user is on the "/course_catalog/edit" page
        And the edited courses have valid names and periods
        And the user clicks "Save"
        Then the changes are saved to the course catalog
        And the user is returned to the "/course_catalog" page which displays the changed course catalog

    Scenario: Add new course to the catalog with unsaved changes to existing courses
        When there are courses in the course catalog
        And the user is on the "/course_catalog/edit" page
        And there is a valid course name and period in the add course fields 
        And there are unsaved changes to the existing course catalog
        And the user clicks "Add"
        Then the "/course_catalog/edit" page is displayed again with the new course included in the course catalog section 
        And the unsaved changes discarded

    Scenario: Save changes to existing courses with a non-empty course name and period in the add section
        When there are courses in the course catalog
        And the user is on the "/course_catalog/edit" page
        And the edited courses have valid names and periods
        And the user has provided a course name and period in the fields used to add a course to the course catalog
        And the user clicks "Save"
        Then the user is returned to the "/course_catalog" page
        And the changes are saved to the course catalog
        And the course name and period are discarded

