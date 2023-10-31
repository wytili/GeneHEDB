import React, { useState, useEffect } from 'react';
import { Input, Button, message, Card, Statistic, Row, Col, Anchor, Table, Radio} from 'antd';
import * as api from './API'; // 引入api.js

const { Link } = Anchor;

const CardStyle = {
  width: 500,
  margin: '20px',
  textAlign: 'center',
  display: 'flex',
  flexDirection: 'column',
  border: '1px solid #096dd9',
  borderRadius: '15px',
};

const App = () => {
  const [data, setData] = useState("");
  const [decryptedData, setDecryptedData] = useState("");
  const [deleteId, setDeleteId] = useState("");
  const [updateId, setUpdateId] = useState("");
  const [cutId, setCutId] = useState("");
  const [allData, setAllData] = useState([]);
  const [stats, setStats] = useState({ total_count: 0, latest_data: "" });
  const [queryGeneId, setQueryGeneId] = useState('');
  const [mutateGeneId, setMutateGeneId] = useState('');
  const [newGeneSequence, setNewGeneSequence] = useState('');
  const [baseType, setBaseType] = useState('A');
  const [firstGene, setFirstGene] = useState('');
  const [secondGene, setSecondGene] = useState('');
  const [startCut, setStartCut] = useState('');
  const [endCut, setEndCut] = useState('');

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Decrypted Gene Sequence',
      dataIndex: 'decrypted',
      key: 'decrypted',
    },
  ];

  useEffect(() => {
    api.getStats().then(setStats);
  }, []);

  const handleEncrypt = async () => {
    try {
      await api.addGeneSequence(data);
      message.success("加密并保存成功");
      api.getStats().then(setStats);
    } catch (error) {
      message.error("加密失败: " + error.message);
    }
    setData("");
  };
  
  const handleDecrypt = async (id) => {
    try {
      const decrypted = await api.getGeneSequence(id);
      setDecryptedData(decrypted);
      message.success(`第${id}个基因序列为 ${decrypted.gene_sequence}`);
    } catch (error) {
      message.error("解密失败: " + error.message);
    }
    setQueryGeneId("");
  };

  const handleDelete = async () => {
    try {
      const result = await api.deleteGeneSequence(deleteId);
      if (result.status === 'success') {
        message.success("删除成功");
        api.getStats().then(setStats);
      } else {
        message.error("删除失败: " + result.message);
      }
    } catch (error) {
      message.error("删除失败: " + error.message);
    }
    setDeleteId("");
  };

  const handleUpdate = async () => {
    try {
      const mutationData = {
        mutation_data: {
          index: parseInt(mutateGeneId)-1,
          new_base: newGeneSequence
        }
      };
      await api.mutateGeneSequence(updateId, mutationData);
      message.success("更新成功");
      api.getStats().then(setStats);
    } catch (error) {
      message.error("更新失败: " + error.message);
    }
    setUpdateId("");
    setMutateGeneId("");
    setNewGeneSequence("");
  };

  const handleGetAll = async () => {
    try {
      const response = await api.getAllGeneSequences();
      if (response && response.all_decrypted_gene_sequences) {
        setAllData(response.all_decrypted_gene_sequences);
      } else {
        message.error("响应不包含 'all_decrypted_gene_sequences'");
      }
    } catch (error) {
      message.error("获取所有基因序列失败: " + error.message);
    }
  };
  

  const handleCompute = async () => {
    try {
      const frequency = await api.computeBaseFrequency(baseType);
      const percentage = await api.computeBasePercentage(baseType);
      message.success(`碱基${baseType}的出现次数是 ${frequency.frequency}，出现频率是 ${percentage.percentage}%`);
    } catch (error) {
      message.error("计算碱基频率失败: " + error.message);
    }
  };

  const handleConcatGene = async () => {
    try {
      await api.concatenateGeneSequences(firstGene, secondGene);
    message.success("基因序列已拼接");
    api.getStats().then(setStats);
    } catch (error) {
      message.error("基因序列拼接失败: " + error.message);
    }
    setFirstGene("");
    setSecondGene("");
  };

  const handleCutGene = async () => {
    try {
      const subSequence = {
          start: parseInt(startCut)-1,
          end: parseInt(endCut)
        }
      await api.deleteSubsequence(cutId, subSequence);
    message.success("基因序列已切除");
    api.getStats().then(setStats);
    } catch (error) {
      message.error("基因序列切除失败: " + error.message);
    }
    setCutId("");
    setStartCut("");
    setEndCut("");
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '50px'}}>
    <div>
    <Anchor style={{ position: 'fixed', top: 0, left: 350, height:"50px", paddingTop:'20px',
      justifyItems: 'center', zIndex: 1000,  backgroundColor:'#fff'}} 
      direction='horizontal' targetOffset={250} offsetTop={500}>
        <Link href="#stats" title="统计数据" />
        <Link href="#addGene" title="增加基因序列" />
        <Link href="#deleteGene" title="删除基因序列" />
        <Link href="#queryGene" title="查询某个基因序列" />
        <Link href="#allGenes" title="查询所有基因序列" />
        <Link href="#mutateGene" title="修改某个基因数据" />
        <Link href="#frequency" title="计算碱基频率" />
        <Link href="#concatGene" title="基因序列拼接" />
        <Link href="#cutGene" title="基因序列切除" />
    </Anchor>

  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '20px' }}> 

    <Row>
        <Col span={12}>
          {/* 查询所有基因序列 */}
          <Card style={CardStyle} title="查询所有基因序列" id="allGenes">
              <Button onClick={handleGetAll}>
                查询所有
              </Button>
              <Table dataSource={allData} columns={columns} pagination={{ pageSize: 20 }} style={{ marginTop: '20px' }} />
          </Card>
        </Col>

        <Col span={12}>
          {/* 统计数据 */}
          <Card style={CardStyle} title="统计数据" id="stats">
              <Row gutter={16}>
                <Col span={12}>
                  <Statistic title="基因序列总数" value={stats.total_count} />
                </Col>
                <Col span={12}>
                  <Statistic title="最新基因序列" value={stats.latest_data} />
                </Col>
              </Row>
            </Card>
          {/* 增加基因序列 */}
          <Card style={CardStyle} title="增加基因序列" id="addGene">
              <Input
                placeholder="输入基因序列（由A/T/G/C构成的字符串）"
                value={data}
                onChange={e => setData(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Button onClick={handleEncrypt}>
                添加基因序列
              </Button>
          </Card>

          {/* 删除基因序列 */}
          <Card style={CardStyle} title="删除基因序列" id="deleteGene">
              <Input
                placeholder="输入要删除的基因序列ID"
                value={deleteId}
                onChange={e => setDeleteId(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Button onClick={handleDelete}>
                删除基因序列
              </Button>
          </Card>

          {/* 查询某个基因序列 */}
          <Card style={CardStyle} title="查询某个基因序列" id="queryGene">
              <Input
                placeholder="输入基因序列ID"
                value={queryGeneId}
                onChange={e => setQueryGeneId(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Button onClick={() => handleDecrypt(queryGeneId)}>

                查询
              </Button>
          </Card>

          

          {/* 修改某个基因数据 */}
          <Card style={CardStyle} title="修改某个基因数据" id="mutateGene">
              <Input
                placeholder="输入基因序列ID"
                value={updateId}
                onChange={e => setUpdateId(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Input
                placeholder="输入变异的碱基位置（index从1开始）"
                value={mutateGeneId}
                onChange={e => setMutateGeneId(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Input
                placeholder="输入变异的碱基数据"
                value={newGeneSequence}
                onChange={e => setNewGeneSequence(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Button onClick={handleUpdate}>
                修改
              </Button>
          </Card>

          {/* 计算某种碱基出现的频率 */}
          <Card style={CardStyle} title="计算某种碱基出现的频率" id="frequency">
              <Radio.Group onChange={e => setBaseType(e.target.value)} value={baseType}>
                <Radio value={'A'}>A</Radio>
                <Radio value={'T'}>T</Radio>
                <Radio value={'G'}>G</Radio>
                <Radio value={'C'}>C</Radio>
              </Radio.Group>
              <Button onClick={handleCompute}>
                计算
              </Button>
          </Card>

          {/* 基因序列拼接 */}
          <Card style={CardStyle} title="基因序列拼接" id="concatGene">
              <Input
                placeholder="输入第一个基因序列"
                value={firstGene}
                onChange={e => setFirstGene(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Input
                placeholder="输入第二个基因序列"
                value={secondGene}
                onChange={e => setSecondGene(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Button onClick={handleConcatGene}>
                拼接
              </Button>
          </Card>

          {/* 基因序列切除 */}
          <Card style={CardStyle} title="基因序列切除" id="cutGene">
              <Input
                placeholder="输入需要切除的基因序列id"
                value={cutId}
                onChange={e => setCutId(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Input
                placeholder="输入起始位置（index从1开始）"
                value={startCut}
                onChange={e => setStartCut(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Input
                placeholder="输入结束位置（要切除的最后一个碱基的index）"
                value={endCut}
                onChange={e => setEndCut(e.target.value)}
                style={{ marginBottom: '10px' }}
              />
              <Button onClick={handleCutGene}>
                切除
              </Button>
          </Card>
        </Col>
    </Row>

      
          
      

          </div>
        </div>
    </div>
  );
};

export default App;
