- [ ] # GeneHEDB

  Application of Homomorphic Encryption in Database Security

  GeneHEDB is a web application that demonstrates the use of homomorphic encryption for securing genetic data in a database. This repository contains both the front-end and back-end components of the application. The front-end is built using React, while the back-end is developed in Python. Additionally, an attack simulation is provided to showcase the security measures implemented in this project.

  ## Front-end

  ### Environment

  The front-end of this project is built using React and relies on the following main dependencies:

  - Node.js: `18.18.0`
  - React: `18.2.0`
  - Create-react-app: `5.0.1`
  - Antd: `5.10.2`

  ### Usage

  To get started with the front-end, follow these steps:

  1. Install project dependencies using the following command:

     ```
     npm install
     ```

  2. Run the project locally using the following command:

     ```
     npm start
     ```

  3. Open [http://localhost:3000](http://localhost:3000/) in your browser to access the front-end of the application.

  ## Back-end

  ### Environment

  The back-end of this project is built using Python and relies on the following main dependencies:

  - Python: `3.8+`
  - Sqlite3: `3.39.3`
  - Flask: `1.1.2`
  - Flask-cors: `4.0.0`
  - TenSEAL: `0.3.14`

  ### Usage

  To set up the back-end, follow these steps:

  1. Install project dependencies using the following command:

     ```
     pip install -r requirements.txt
     ```

  2. Run the project, and the database will be ready for use.

     ```
     python app.py
     ```

  ## Attack Simulation

  ### SQL Injection

  This application includes an attack simulation feature to demonstrate the effectiveness of the implemented security measures. To simulate an SQL injection attack, you can visit the following URL in your browser:

  ```
  http://localhost:5000/unsafe_query?search=anything' OR '1'='1' --
  ```

  By visiting this URL, you can observe that the data is encrypted and protected from SQL injection attacks.

  ## Homomorphic Encryption Demonstration

  In the root directory of the project, you will find a `test.py` file that demonstrates simple algorithms for performing addition, subtraction, and multiplication using homomorphic encryption. You can run this script to understand the principles and examples of homomorphic encryption.

  ## Todo List

  - [x] 基因序列增删查
  - [x] 显示数据库表格
  - [x] 计算某种碱基出现频率
  - [x] 变异
  - [x] 拼接
  - [x] 切除
  - [x] 模拟SQL注入攻击
  - [x] 加入相似基因序列查询功能
  - [x] 考虑查询时是否要遵循人性化设置将index + 1
  - [x] 考虑切除时是否要遵循人性化设置将start - 1，end + 1
  - [ ] 美化页面样式——拟态风格？删去Tabs改为row&col？
  - [ ] More functions？
  - [ ] More attacks?

  

  ## GitHub Repository

  You can find the GitHub repository for this project [here](https://github.com/wytili/GeneHEDB). Feel free to contribute and enhance the functionality and security of this application. 

  ## Contributors

  Special thanks to the following contributors for their valuable contributions to this project:

  - [Yiting Wang](https://github.com/wytili)
  - [Hexi Wang](https://github.com/halsayxi)
  - [Can Liu](https://github.com/ccliu-u)
