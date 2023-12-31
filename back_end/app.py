from flask import Flask, request, jsonify
import tenseal as ts
from db import init_db, insert_data, fetch_data, fetch_all_data, get_data_count, get_latest_data, update_data, \
    delete_data, unsafe_query
from flask_cors import CORS
import numpy as np
import random
from Bio import Align

app = Flask(__name__)
CORS(app)  # 为所有接口启用跨域

# 基因序列碱基与数字的正反映射，便于操作
mapping = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
reverse_mapping = {0: 'A', 1: 'T', 2: 'G', 3: 'C'}

# 同态加密参数初始化
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2 ** 40
context.generate_galois_keys()

init_db()


# 数据库初始化随机生成序列
def add_gene_sequence_init(gene_sequence):
    mapped_sequence = [mapping[gene] for gene in gene_sequence]
    # 数据加密
    encrypted_vector = ts.ckks_vector(context, mapped_sequence)

    # 存储加密数据
    insert_data(encrypted_vector.serialize())


# 在数据库中添加随机生成的基因序列
for _ in range(20):
    random_sequence = ''.join(random.choice('ATCG') for _ in range(8))
    add_gene_sequence_init(random_sequence)


# 增：添加一段新的基因序列
@app.route('/encrypt', methods=['POST'])
def add_gene_sequence():
    gene_sequence = request.json['gene_sequence']
    mapped_sequence = [mapping[gene] for gene in gene_sequence]

    # 数据加密
    encrypted_vector = ts.ckks_vector(context, mapped_sequence)

    insert_data(encrypted_vector.serialize())
    return jsonify({"status": "success", "message": "Gene sequence added"}), 200


# 删：删除一段异常或不再需要的基因序列
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_gene_sequence(id):
    rows_affected = delete_data(id)
    if rows_affected == 0:
        return jsonify({"status": "failed", "message": f"No gene sequence with ID {id} found"}), 404
    else:
        return jsonify({"status": "success", "message": f"Gene sequence with ID {id} deleted"}), 200


# 查：解密并获取一段特定基因序列
@app.route('/decrypt/<int:id>', methods=['GET'])
def get_gene_sequence(id):
    encrypted_data = fetch_data(id)

    # 解密数据并转换回基因序列
    encrypted_vector = ts.ckks_vector_from(context, encrypted_data)
    decrypted_vector = encrypted_vector.decrypt()
    gene_sequence = ''.join([reverse_mapping[int(round(x))] for x in decrypted_vector])

    return jsonify({"gene_sequence": gene_sequence}), 200


# 查询所有
@app.route('/get_all', methods=['GET'])
def get_all_gene_sequences():
    all_encrypted_sequences = fetch_all_data()
    if not all_encrypted_sequences:
        return jsonify({"error": "No encrypted sequences found"}), 400

    try:
        decrypted_sequences = []
        for item in all_encrypted_sequences:
            # 查看字典中是否存在encrypted键
            if 'encrypted' in item:
                try:
                    encrypted_vector = ts.ckks_vector_from(context, item['encrypted'])
                except Exception as e:
                    print(f"Skipping an item due to exception: {e}")
                    continue
            else:
                print(f"Skipping an item due to unexpected type or structure: {item}")
                continue

            decrypted_vector = encrypted_vector.decrypt()
            rounded_vector = np.round(decrypted_vector).astype(int)
            gene_sequence = ''.join([reverse_mapping[x] for x in rounded_vector])
            decrypted_sequences.append({"id": item["id"], "decrypted": gene_sequence})

        return jsonify({"all_decrypted_gene_sequences": decrypted_sequences}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 改：对一个已存在的基因序列进行变异（Mutation）
@app.route('/mutate/<int:id>', methods=['PUT'])
def mutate_gene_sequence(id):
    mutation_data = request.json['mutation_data']  # 输入形式可以是 {'index': 3, 'new_base': 'A'}

    # 获取原来的加密数据
    encrypted_data = fetch_data(id)
    encrypted_vector = ts.ckks_vector_from(context, encrypted_data)
    decrypted_vector = encrypted_vector.decrypt()

    # 执行基因变异，然后重新加密
    original_sequence = [reverse_mapping[int(round(x))] for x in decrypted_vector]
    original_sequence[mutation_data['index']] = mutation_data['new_base']
    new_mapped_sequence = [mapping[base] for base in original_sequence]
    new_encrypted_vector = ts.ckks_vector(context, new_mapped_sequence)

    # 更新数据库
    update_data(id, new_encrypted_vector.serialize())
    return jsonify({"status": "success", "message": f"Gene sequence with ID {id} mutated"}), 200


# 算：统计某个碱基（A、T、G、C）在所有序列中出现的次数
@app.route('/compute_frequency', methods=['POST'])
def compute_base_frequency():
    target_base = request.json["target_base"]  # 'A', 'T', 'G', 'C'
    target_value = mapping[target_base]

    all_encrypted_sequences = fetch_all_data()
    frequency = 0

    for encrypted_data in all_encrypted_sequences:
        # 查看字典中是否存在encrypted键
        if isinstance(encrypted_data, dict) and 'encrypted' in encrypted_data:
            try:
                encrypted_vector = ts.ckks_vector_from(context, encrypted_data['encrypted'])
            except Exception as e:
                print(f"Skipping an item due to exception: {e}")
                continue
        else:
            print(f"Skipping an item due to unexpected type or structure: {encrypted_data}")
            continue

        decrypted_vector = encrypted_vector.decrypt()
        # 转换为整数
        rounded_vector = np.round(decrypted_vector).astype(int)
        # 计算目标碱基出现的次数
        frequency += np.count_nonzero(rounded_vector == target_value)

    return jsonify({"status": "success", "frequency": frequency, "target_base": target_base}), 200


# 算：统计某个碱基（A、T、G、C）在所有序列中出现的概率
@app.route('/compute_percentage', methods=['POST'])
def compute_base_percentage():
    target_base = request.json["target_base"]  # 'A', 'T', 'G', 'C'
    target_value = mapping[target_base]

    all_encrypted_sequences = fetch_all_data()
    total_bases = 0  # 用于计算总碱基数
    target_count = 0  # 用于计算目标碱基的数量

    for encrypted_data in all_encrypted_sequences:
        # 查看字典中是否存在encrypted键
        if isinstance(encrypted_data, dict) and 'encrypted' in encrypted_data:
            try:
                encrypted_vector = ts.ckks_vector_from(context, encrypted_data['encrypted'])
            except Exception as e:
                print(f"Skipping an item due to exception: {e}")
                continue
        else:
            print(f"Skipping an item due to unexpected type or structure: {encrypted_data}")
            continue

        decrypted_vector = encrypted_vector.decrypt()
        # 转换为整数
        rounded_vector = np.round(decrypted_vector).astype(int)
        # 计算目标碱基出现的次数
        target_count += np.count_nonzero(rounded_vector == target_value)
        total_bases += len(rounded_vector)

    # 计算目标碱基出现的概率百分比
    percentage = (target_count / total_bases) * 100

    return jsonify({"status": "success", "percentage": percentage, "target_base": target_base}), 200


# 基因序列拼接
@app.route('/concatenate/<int:id1>/<int:id2>', methods=['POST'])
def concatenate_gene_sequences(id1, id2):
    encrypted_data1 = fetch_data(id1)
    encrypted_data2 = fetch_data(id2)
    encrypted_vector1 = ts.ckks_vector_from(context, encrypted_data1)
    encrypted_vector2 = ts.ckks_vector_from(context, encrypted_data2)

    decrypted_vector1 = encrypted_vector1.decrypt()
    decrypted_vector2 = encrypted_vector2.decrypt()

    concatenated_sequence = decrypted_vector1 + decrypted_vector2

    # 重新加密拼接后的序列
    new_encrypted_vector = ts.ckks_vector(context, concatenated_sequence)

    # 存入数据库
    insert_data(new_encrypted_vector.serialize())

    return jsonify({"status": "success", "message": f"Gene sequences with IDs {id1} and {id2} concatenated"}), 200


# 基因序列切除
@app.route('/delete_subsequence/<int:id>', methods=['POST'])
def delete_subsequence(id):
    subsequence_info = request.json  # 输入形式可以是 {'start': 3, 'end': 5}

    encrypted_data = fetch_data(id)
    encrypted_vector = ts.ckks_vector_from(context, encrypted_data)
    decrypted_vector = encrypted_vector.decrypt()

    # 执行基因序列的切除
    del decrypted_vector[subsequence_info['start']:subsequence_info['end']]

    # 重新加密
    new_encrypted_vector = ts.ckks_vector(context, decrypted_vector)

    # 更新数据库
    update_data(id, new_encrypted_vector.serialize())

    return jsonify({"status": "success", "message": f"Subsequence deleted from gene sequence with ID {id}"}), 200


# 统计：获取数据库中的基因序列总数和最新基因序列
@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        # 获取统计信息
        count = get_data_count()

        encrypted_data = get_latest_data()
        encrypted_vector = ts.ckks_vector_from(context, encrypted_data)
        decrypted_vector = encrypted_vector.decrypt()
        original_sequence = [reverse_mapping[int(round(x))] for x in decrypted_vector]
        original_sequence_str = ''.join(original_sequence)
        return jsonify({"total_count": count, "latest_data": original_sequence_str}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 计算序列相似度 - 局部比对
# 此处函数的修改只是因为旧的Bio.pairwise2模块已经被弃用，所以改为Bio.Align.PairwiseAligner来重写
def sequence_similarity(seq1, seq2):
    # 创建 PairwiseAligner 对象
    aligner = Align.PairwiseAligner()
    # 设置对齐方法为 local
    aligner.mode = 'local'
    # 设置得分规则：匹配得分为1，不匹配和空位得分为0
    aligner.match_score = 1
    aligner.mismatch_score = 0
    aligner.open_gap_score = 0
    aligner.extend_gap_score = 0

    # 进行序列对齐
    alignments = aligner.align(seq1, seq2)

    # 选择得分最高的对齐方式
    top_alignment = max(alignments, key=lambda x: x.score)
    # 计算相似度比例
    similarity = top_alignment.score / min(len(seq1), len(seq2))
    return similarity


# 查找相似基因序列
@app.route('/fuzzy_search', methods=['POST'])
def fuzzy_search():
    input_sequence = request.json['gene_sequence']
    all_encrypted_sequences = fetch_all_data()

    results = []

    for item in all_encrypted_sequences:
        if 'encrypted' in item and 'id' in item:
            encrypted_vector = ts.ckks_vector_from(context, item['encrypted'])
            decrypted_vector = encrypted_vector.decrypt()
            gene_sequence = ''.join([reverse_mapping[int(round(x))] for x in decrypted_vector])

            similarity = sequence_similarity(input_sequence, gene_sequence)
            results.append({
                "id": item['id'],
                "sequence": gene_sequence,
                "similarity": similarity
            })

    # 根据相似度对结果进行排序，并显示相似度最高的五个
    results = sorted(results, key=lambda x: x['similarity'], reverse=True)[:5]

    return jsonify(results), 200


# 不安全的查询：用于演示SQL注入攻击
@app.route('/unsafe_query', methods=['GET'])
def sql_attack():
    try:
        search_term = request.args.get('search')
        encrypted_data = unsafe_query(search_term)
        simplified_data = [str(item)[:1000] + "..." for item in encrypted_data]  # 只显示前1000个字符和省略号
        return jsonify({"status": "success", "data": simplified_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
