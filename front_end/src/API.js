// Note: API 接口定义
const API_URL = 'http://127.0.0.1:5000'; // 后端地址

// 添加基因序列
export const addGeneSequence = async (sequence) => {
  const response = await fetch(`${API_URL}/encrypt`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ gene_sequence: sequence }),
  });

  return await response.json();
};

// 删除基因序列
export const deleteGeneSequence = async (id) => {
  const response = await fetch(`${API_URL}/delete/${id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error(`Failed to delete gene sequence with ID ${id}`);
  }

  return await response.json();
};

// 查询基因序列
export const getGeneSequence = async (id) => {
  const response = await fetch(`${API_URL}/decrypt/${id}`, {
    method: 'GET',
  });

  return await response.json();
};

// 查询所有基因序列
export const getAllGeneSequences = async () => {
  const response = await fetch(`${API_URL}/get_all`, {
    method: 'GET',
  });

  return await response.json();
};

// 基因序列变异
export const mutateGeneSequence = async (id, mutationData) => {
  const response = await fetch(`${API_URL}/mutate/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(mutationData),
  });

  if (!response.ok) {
    throw new Error(`Failed to mutate gene sequence with ID ${id}`);
  }

  return await response.json();
};


// 计算碱基频率
export const computeBaseFrequency = async (baseType) => {
  const response = await fetch(`${API_URL}/compute_frequency`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ target_base: baseType }),
  });

  return await response.json();
};

// 拼接基因序列
export const concatenateGeneSequences = async (id1, id2) => {
  const response = await fetch(`${API_URL}/concatenate/${id1}/${id2}`, {
    method: 'POST',
  });

  return await response.json();
};

// 基因序列切除
export const deleteSubsequence = async (id, subsequenceInfo) => {
  const response = await fetch(`${API_URL}/delete_subsequence/${id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(subsequenceInfo),
  });

  return await response.json();
};

// 基因序列总数统计和最新基因序列
export const getStats = async () => {
  const response = await fetch(`${API_URL}/stats`, {
    method: 'GET',
  });

  return await response.json();
};
