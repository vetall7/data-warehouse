<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
<!--   <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">Data warehouse for school</h3>

  <p align="center">
    Design and implementation of data warehouse for school
    <br />
    <a href="#demo">View Demo</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href='#demo'>Demo</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>




<!-- ABOUT THE PROJECT -->
## About The Project

The primary objective of this project is to design and implement a data warehouse to support the school's business processes.

Key stages of the work:
* Defining requirements for the BI system and preparing data sources, including designing the school's database.
  
  ![image](https://github.com/user-attachments/assets/f83d4f55-f671-4db3-be0d-02f9c577e0dc)

* Developing a data generator to produce large volumes of mock data and implementing bulk inserts for efficient data loading.
* Designing the data warehouse architecture.
* Implementing the data warehouse, including defining measures, dimensions, and other key components.
* Implementing the ETL process, primarily using T-SQL.
* Writing queries in MDX to analyze data within the data warehouse.
* Testing the data warehouse across different OLAP models (MOLAP, HOLAP, ROLAP).
* Creating a Power BI dashboard for data visualization and analysis.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With
<p> <a href="https://pypi.org/project/Faker/"><img src="https://skillicons.dev/icons?i=py" /></a> The Faker library is used to generate a large volume of realistic mock data. Additionally, a separate script handles database connections and efficiently performs bulk data loading.  </p> 

<p> <a href="https://www.microsoft.com/en-us/sql-server" target="_blank" rel="noreferrer"> <img src="https://www.svgrepo.com/show/303229/microsoft-sql-server-logo.svg" alt="mssql" width="40" height="40"/> </a> Microsoft SQL Server serves as the storage solution for both the school database and the data warehouse </p>
<p> <a href="https://en.wikipedia.org/wiki/Transact-SQL">T-SQL</a> is utilized for implementing the ETL process, including loading data from various sources (relational databases and .csv files), transforming it to achieve the required structure, and inserting it into the data warehouse. </p>


</p>
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Demo


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact

Vitalii Shapovalov - [@LinkedIn](https://www.linkedin.com/in/vitalii-shapovalov-6670ba26a/) - shapovalovvit0@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Transact-SQL](https://en.wikipedia.org/wiki/Transact-SQL)
* [Data warehouses](https://cloud.google.com/learn/what-is-a-data-warehouse)
* [Facts and measures](https://www.toucantoco.com/en/blog/differences-facts-measures-metrics)
* [Faker python](https://pypi.org/project/Faker/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
