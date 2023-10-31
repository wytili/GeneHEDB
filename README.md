# GeneHEDB

Application of Homomorphic Encryption in Database Security

## Front-end 

### Environment

This project is built using React and relies on the following main dependencies:

- Node.js:`18.18.0`
- React: `18.2.0` 
- Create-react-app:`5.0.1`
- Antd: `5.10.2`

### usage

You can install project dependencies using the following command:

```
npm install
```

You can run the project locally using the following command:

```
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Back-end

### Environment

This project is built using Python and relies on the following main dependencies:

- Python:`3.8+`
- Sqlite3:`3.39.3`
- Flask: `1.1.2` 
- Flask-cors: `4.0.0`
- TenSEAL:`0.3.14`

### usage

You can install project dependencies using the following command:

```
pip install -r requirements.txt
```

Then run the project and the database is ready.

## Attack Simulation

### SQL Injection 

Visit `http://localhost:5000/unsafe_query?search=anything' OR '1'='1' --` or some other address with a browser to find out that the data is encrypted.

## TODO

- [x] 基因序列增删查
- [x] 显示数据库表格
- [x] 计算某种碱基出现频率
- [x] 变异
- [x] 拼接
- [x] 切除
- [x] **模拟SQL注入攻击**
- [ ] More functions？如计算两个基因序列的相似度
- [ ] More attacks？
- [x] 考虑查询时是否要遵循人性化设置将index + 1
- [x] 考虑切除时是否要遵循人性化设置将start - 1，end + 1
- [ ] 美化页面样式——拟态风格？删去Tabs改为row&col？
