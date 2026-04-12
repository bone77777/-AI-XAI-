class XaiPrescriptiveAgent:
    def __init__(self):
        # 1. 重み設定（学習済みモデルのパラメータを想定）
        self.feature_weights = {
            "traffic_volume": 0.7,      # 通信量が多い (+)
            "ti_reputation": 0.4,       # TIが疑わしい (+)
            "valid_signature": -0.8,    # 署名が有効 (-)
            "internal_process": -0.5    # 正規プロセス (-)
        }
        
        # 2. アクションの定義（処方的AIの選択肢）
        self.actions = {
            "ISOLATE": {"name": "完全遮断", "defense": 1.0, "cost": 100},
            "THROTTLE": {"name": "帯域制限", "defense": 0.6, "cost": 15},
            "MONITOR": {"name": "監視のみ", "defense": 0.1, "cost": 2}
        }

    def analyze(self, logs, business_context):
        # --- [STEP 1: XAIによる予測と根拠の可視化] ---
        contributions = {}
        risk_score = 0
        
        for feature, weight in self.feature_weights.items():
            value = logs.get(feature, 0)
            contribution = value * weight
            contributions[feature] = contribution
            risk_score += contribution
        
        risk_score = max(0, min(1, risk_score)) # 0-1に正規化
        
        print("【XAI：判定根拠の可視化】")
        for f, c in contributions.items():
            mark = "🚨" if c > 0 else "✅"
            print(f"  {mark} {f:16}: {c:+.2f}")
        print(f"  => 最終リスク確信度: {risk_score:.2%}\n")

        # --- [STEP 2: 処方的AIによるアクション最適化] ---
        # 資産価値と「決算期」による重み付け
        asset_value = 100
        if business_context.get("is_closing_period"):
            asset_value *= 2.0 # 決算期は可用性のコストが倍増
            
        best_action = None
        max_utility = -float('inf')
        prescriptive_reason = ""

        print("【処方的AI：アクションのシミュレーション】")
        for key, act in self.actions.items():
            # ユーティリティ = (防げるリスク) - (ビジネス停止コスト)
            mitigated_risk = risk_score * asset_value * act["defense"]
            business_loss = asset_value * (act["cost"] / 100) # コストが高いほど業務停止リスク大
            
            utility = mitigated_risk - business_loss
            print(f"  - {act['name']:8}: 有益性スコア {utility:+.2f}")
            
            if utility > max_utility:
                max_utility = utility
                best_action = act
                prescriptive_reason = (
                    f"リスク({risk_score:.1%})に対して、"
                    f"業務停止損失({business_loss:.1f})を最小化しつつ、"
                    f"防御効果({act['defense']:.0%})を最大化できるため。"
                )

        print(f"\n【最終処方箋】")
        print(f"推奨アクション: {best_action['name']}")
        print(f"処方理由: {prescriptive_reason}")

# --- 実行シミュレーション ---

# 1. ログデータ（今回のインシデント）
log_data = {
    "traffic_volume": 1.0,     # 大量通信あり
    "ti_reputation": 0.5,      # サブネットがヒット（中程度の疑い）
    "valid_signature": 1.0,    # 署名あり（強い白要素）
    "internal_process": 1.0    # 正規プロセス（白要素）
}

# 2. ビジネスコンテキスト（経理部の決算期）
context = {"is_closing_period": True}

# 実行
agent = XaiPrescriptiveAgent()
agent.analyze(log_data, context)