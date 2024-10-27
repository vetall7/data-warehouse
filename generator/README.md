# Springfield School Data Generator

This tool generates mock data for Springfield School based on a predefined schema. Refer to the `/docs` folder for more details on the schema.

## Usage

1. **Configure the Generator**:
    - Edit the `config.yml` file to set the number of data entries, field values, time periods, and other parameters.
    - Note: Do not confuse `config.yml` with `src/config.py`.

2. **Run the Generator**:
    ```sh
    pip install -r requirements.txt
    python3 main.py
    ```

3. **Access Generated Data**:
    - The generated data will be stored in the `data` folder.
    - Each time period will have its own subfolder.
    - Data will be saved in CSV format, with filenames corresponding to table names.

## Project Structure

- `src` - Source code of the generator
  - `requirements.txt` - List of dependencies
  - `main.py` - Entry point of the generator
  - `generator.py` - Main generator class
  - `config.py` - Configuration file
  - `tables.py` - Table classes
  - `utils.py` - Utility functions
- `data` - Folder for generated data
- `config.yml` - Main configuration file
