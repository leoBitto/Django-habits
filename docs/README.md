# Habits App

Questo progetto Django è progettato per aiutarti a gestire e monitorare le tue abitudini quotidiane.

## Models
The main entities of the system are represented by the following models:

### Category
The Category model represents a category to which a habit can be associated. Each category has a name, a default color, and an optional icon.

### Habit
The Habit model represents a habit and can be associated with a specific category through a ForeignKey relationship. Each habit has a unique name, a category, and a boolean field is_positive indicating whether the habit is considered positive or negative. If a habit is positive, the goal can be considered achieved if the number of completed events is above the target. If a habit is negative, the goal can be considered achieved if the number of completed events is below the target.

### HabitEvent
The HabitEvent model tracks specific events related to the habit. Each event has a reference to the associated habit, a date, an optional time, an optional location, and a boolean status completed indicating whether the habit was completed during that event.

## View
The overview view provides an overview of statistics related to habits and habit events. It calculates various statistics, including the total number of habits, total events, and the average number of events per habit. It then creates Plotly charts for visualization and passes the data to the template.

### Category Views
#### Category List View
The category view fetches all categories, creates a form for category creation, and prepares a dictionary of edit forms for each category. It then renders the category.html template with the context.

#### Create Category View
The create_category view handles the creation of a new category and redirects the user to the category list view (category).

#### Edit and Delete Category Views
The edit_category view handles the editing of categories, and the delete_category view handles the deletion of categories. After successful editing or deletion, the user is redirected to the category list view (category).

### Habit Views
#### Habit List View
The habit view fetches all habits, creates a form for habit creation, and prepares a dictionary of edit forms for each habit. Additionally, it groups habits by category for better organization and presentation. The resulting context is used to render the habit.html template.

#### Create, Edit, and Delete Habit Views
These views handle the creation, editing, and deletion of habits. After each operation, the user is redirected to the habit list view (habit).

### Habit Event Views
#### Habit Event List View
The habit_event view fetches all habit events, creates a form for habit event creation, and prepares a dictionary of edit forms for each habit event. It also groups habit events by category for better organization and presentation. The resulting context is used to render the habit_event.html template.

#### Create, Edit, and Delete Habit Event Views
These views handle the creation, editing, and deletion of habit events. After each operation, the user is redirected to the habit event list view (habit_event).

This README provides an overview of the Django Habits App views. Each section describes the purpose and functionality of a specific view, helping you understand and manage the different aspects of your habits application.



