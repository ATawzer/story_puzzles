Project Muse

## Structure

- `app/` - The main application and UI. Anything related purely to just the UI and user experience. Depends on the `project_muse` library.
- `app/src/` - The source code for the UI `app/` module.
- `project_muse/` - The project muse library. Anything related to the core functionality of the project, this is meant to be a functional template for the C++ version of the project. There should be no dependencies on the UI from this library.

### Project Muse

#### Templates
This is the datbase connected features and represent the key configurable pieces of the project. These are used for a factory style pattern at runtime to generate the final product but are otherwise persistent and not needed at runtime. They are, however, used in the editor to configure the project.



