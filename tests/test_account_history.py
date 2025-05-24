from utils.account_history import AccountHistoryAnalyzer

analyzer = AccountHistoryAnalyzer(max_posts=5)


def test_fetch_post_history():
    posts = analyzer.fetch_post_history("user", "youtube")
    assert len(posts) == 5


def test_analyze_history():
    stats = analyzer.analyze_history("user", "youtube")
    assert stats["post_count"] == 5.0
