import tenseal as ts


def homomorphic_computation(data_1, data_2, op):
    # 设置同态加密的参数
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2 ** 40
    context.generate_galois_keys()

    # 加密数据
    encrypted_data1 = ts.ckks_vector(context, data_1)
    encrypted_data2 = ts.ckks_vector(context, data_2)

    # 根据用户选择的操作，在数据被加密的状态下对其进行计算
    if op == 'add':
        encrypted_result = encrypted_data1 + encrypted_data2
    elif op == 'sub':
        encrypted_result = encrypted_data1 - encrypted_data2
    elif op == 'mul':
        encrypted_result = encrypted_data1 * encrypted_data2
    else:
        raise ValueError("Unsupported operation")

    # 解密结果
    decrypted_result = encrypted_result.decrypt()
    int_array = [round(x) for x in decrypted_result]

    return int_array


data1 = [float(x) for x in input("输入第一组数据（使用空格分隔）: ").split()]
data2 = [float(x) for x in input("输入第二组数据（使用空格分隔）: ").split()]
operation = input("选择操作（add, sub, mul）: ")


try:
    result = homomorphic_computation(data1, data2, operation)
    print("解密后的结果:", result)
except Exception as e:
    print("发生错误:", e)
