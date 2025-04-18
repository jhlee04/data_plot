import pandas as pd
import numpy as np

# 예제 데이터 불러오기 (예: df = pd.read_excel("응답DB.xlsx"))
# 지금은 예제 데이터프레임 df 가 이미 있다고 가정합니다

# (1) 점수형 & 선택형 분류
def classify_columns(df):
    col_prefixes = df.columns[df.columns.str.contains("_")].map(lambda x: x.split("_")[0])
    duplicated_prefixes = col_prefixes[col_prefixes.duplicated()].unique()
    select_cols = [col for col in df.columns if any(col.startswith(prefix + "_") for prefix in duplicated_prefixes)]
    score_cols = [col for col in df.columns if col not in select_cols + ["부서", "팀"]]
    return score_cols, duplicated_prefixes, select_cols

# (2) 점수형 평균
def get_score_summary(df, score_cols):
    return df.groupby(["부서", "팀"])[score_cols].mean().round(2)

# (3) 선택형 Top3 추출
def get_choice_top3(df, select_prefixes, select_cols):
    results = []
    for (dept, team), group in df.groupby(["부서", "팀"]):
        team_result = {"부서": dept, "팀": team}
        for prefix in select_prefixes:
            group_cols = [col for col in select_cols if col.startswith(prefix + "_")]
            counts = group[group_cols].sum().sort_values(ascending=False)
            for i, (col, count) in enumerate(counts.head(3).items(), 1):
                label = col.split("_", 1)[1]
                team_result[f"{prefix}_Top{i}"] = label
                team_result[f"{prefix}_Top{i}_카운트"] = int(count)
        results.append(team_result)
    return pd.DataFrame(results).set_index(["부서", "팀"])

# (4) 실행 전체
def analyze_survey(df):
    score_cols, select_prefixes, select_cols = classify_columns(df)
    score_df = get_score_summary(df, score_cols)
    select_df = get_choice_top3(df, select_prefixes, select_cols)
    result = pd.concat([score_df, select_df], axis=1)
    return result

# (5) 예제 실행
if __name__ == "__main__":
    # 예제 df 또는 엑셀에서 불러오기
    # df = pd.read_excel("응답DB.xlsx")
    
    # 예시: 당신이 만든 30명짜리 df를 쓴다면
    final_result = analyze_survey(df)
    final_result.to_excel("팀별_설문분석_요약보고서.xlsx")
    print("완료: 결과가 '팀별_설문분석_요약보고서.xlsx'로 저장되었습니다.")
