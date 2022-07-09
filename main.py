
import pandas as pd

datafile = 'data.csv'
correctfile = 'correct.csv'

data = pd.read_csv(datafile, header=None)
correct = pd.read_csv(correctfile, header=None)

# 問題分類
q_num = correct[1].values.tolist()
# 配点
q_scores = correct[2].values.tolist()
# 正解番号
correct = correct[0].values.tolist()

# データの形式をbefore -> after で置換
before = [' "0"', ' "1"', ' "2"', ' "3"', ' "4"',
          ' "5"', ' "6"', ' "7"', ' "8"', ' "9"', ' ""']
after = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, None]
data = data.replace(before, after)

# データの余分な列を削除
correct_N = len(correct)

data = data.iloc[:, :correct_N+1]


# 配点の問題別分類
begin = 0
end = 0
point_allocation = []
# [begin:end]-> begin <= x < end
for n in range(len(q_num)-1):
    diff = q_num[n+1] - q_num[n]
    if diff != 0:
        end = n+1
        point_allocation.append(q_scores[begin:end])
        begin = n+1
#  最後を追加
if len(point_allocation) != q_num[-1]:
    point_allocation.append(q_scores[begin:])


q_len = len(point_allocation)
# 満点を計算
corr_sum = 0
for q in range(len(point_allocation)):
    corr_sum += point_allocation[q][0]


# 正誤判別
rows_N = len(data.index)
columns_N = len(data.columns)
result = []

# 行方向　人
for i in range(rows_N):

    student = {}
    begin = 0
    end = 0
    score = 0
    count = 0
    correct_bool = []
    answer = []
    correct_num = []
    incorrect_num = []
    correct_ans = []
    incorrect_ans = []

    # 列０は学籍番号
    student['Number'] = data[0][i]

    #　列方向　マーク番号
    for j in range(1, columns_N):
        if data[j][i] == correct[j-1]:
            count += 1
            correct_bool.append(True)
            correct_num.append(j)
        else:
            correct_bool.append(False)
            incorrect_num.append(j)

    # マーク番号を問題別に分類して二次元配列で表現する
    for n in range(len(q_num)-1):
        diff = q_num[n+1] - q_num[n]
        if diff != 0:
            end = n+1
            answer.append(correct_bool[begin:end])
            begin = n+1
    if len(answer) != q_num[-1]:
        answer.append(q_scores[begin:])

    # 問題別正解カウント
    for q in range(len(answer)):
        if all(answer[q]):
            correct_ans.append(q+1)
            score += point_allocation[q][0]

        else:
            incorrect_ans.append(q+1)

    # print(correct_bool)
    student['Score'] = score
    student['Count'] = count
    student['CorrectNum'] = correct_num
    student['IncorrectNum'] = incorrect_num
    student['CorrectAns'] = correct_ans
    student['IncorrectAns'] = incorrect_ans
    result.append(student)

# 学生別結果の出力
result_score = []
result_num = []
result_corr = []
result_N = len(result)
for k in range(result_N):

    result_num.append(result[k]["Number"])
    result_score.append(result[k]["Score"])
    result_corr.append(result[k]["CorrectAns"])
    print("-"*20)
    print("学籍番号: ", result[k]["Number"])

    # 問
    print("点数: ", result[k]["Score"], end="")
    print("/"+str(corr_sum)+'点')
    print("正解問題: ", result[k]["CorrectAns"])
    print("不正解問題: ", result[k]["IncorrectAns"])
    print("")
    # マーク番号
    print("正解数: ", result[k]["Count"], end="")
    print("/"+str(correct_N)+'個')
    print("正解マーク番号: ", result[k]["CorrectNum"])
    print("不正解マーク番号: ", result[k]["IncorrectNum"])

# 評価指標
print('='*20)
print('受験者：　　　　'+str(len(result_score))+'人')
print('テスト平均値：　'+str(sum(result_score)/len(result_score))+'点')
print('テスト最高値：　'+str(max(result_score))+'点')
print('テスト最低値：　'+str(min(result_score))+'点')


result_q_all = []
label = []

for name in range(q_len):
    label.append("問"+str(name+1))

for num in range(result_N):
    result_q = [0]*q_len
    for ans in result_corr[num]:
        result_q[ans-1] = point_allocation[ans-1][0]
    result_q_all.append(result_q)

df_q = pd.DataFrame(result_q_all, columns=label)
df_s = pd.DataFrame(result_score, columns=["得点"])
df_result = pd.DataFrame(result_num, columns=["学籍番号"])

df_result = pd.concat([df_result, df_q, df_s], axis=1)
df_result = df_result.set_index('学籍番号')


tag = datafile.split('.')[0]
df_result.to_csv(tag+"_result.csv", encoding="shift_jis")
