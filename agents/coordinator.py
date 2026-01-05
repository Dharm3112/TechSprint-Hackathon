# agents/coordinator.py
def run_flow(complaint):
    # 1. Triage
    category = TriageAgent.classify(complaint)
    
    # 2. Check Memory (RAG)
    similar_cases = VectorMemory.search(complaint)
    
    # 3. Assess Risk
    score = RiskAgent.analyze(complaint, similar_cases)
    
    # 4. Conditional Branching
    if score > 80:
        return EscalationProtocol.execute(complaint, score)
    
    # 5. Draft & Critique Loop
    draft = ActionAgent.draft(complaint, category)
    critique = CriticAgent.review(draft, complaint)
    
    if not critique.passed:
        draft = ActionAgent.rewrite(draft, critique.feedback)
        
    return draft