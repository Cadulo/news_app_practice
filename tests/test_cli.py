# mypy: disable-error-code=unreachable
"""Tests for cli."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from platzi_news.io.cli import main


class TestCLI:
    """Test CLI functions."""

    @patch("platzi_news.io.cli.NewsService")
    @patch("sys.exit")
    @pytest.mark.anyio  # type: ignore[misc]
    async def test_main_search_command(
        self, mock_exit: MagicMock, mock_service_class: MagicMock
    ) -> None:
        """Test main function with search command."""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.asearch_articles = AsyncMock(return_value=[])

        with patch(
            "sys.argv", ["platzi-news", "search", "test", "--source", "guardian"]
        ):
            await main()

        mock_service.asearch_articles.assert_awaited_once_with("guardian", "test")
        mock_exit.assert_called_once_with(0)

    @patch("platzi_news.io.cli.NewsService")
    @patch("sys.exit")
    @pytest.mark.anyio  # type: ignore[misc]
    async def test_main_ask_command(
        self, mock_exit: MagicMock, mock_service_class: MagicMock
    ) -> None:
        """Test main function with ask command."""
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.asearch_articles = AsyncMock(return_value=[])
        mock_service.analyze_articles.return_value = "Answer"

        with patch(
            "sys.argv",
            ["platzi-news", "ask", "test", "question", "--source", "guardian"],
        ):
            await main()

        mock_service.asearch_articles.assert_awaited_once_with("guardian", "test")
        mock_service.analyze_articles.assert_called_once_with([], "question")
        mock_exit.assert_called_once_with(0)

    @patch("sys.exit")
    @pytest.mark.anyio  # type: ignore[misc]
    async def test_main_no_command(self, mock_exit: MagicMock) -> None:
        """Test main with no command."""
        mock_exit.side_effect = SystemExit

        with patch("sys.argv", ["platzi-news"]), pytest.raises(SystemExit):
            await main()

        mock_exit.assert_called_once_with(1)

    @patch("platzi_news.io.cli.NewsService")
    @patch("sys.exit")
    @pytest.mark.anyio  # type: ignore[misc]
    async def test_main_exception_handling(
        self, mock_exit: MagicMock, mock_service_class: MagicMock
    ) -> None:
        """Test main handles exceptions."""
        mock_service_class.side_effect = Exception("Test error")
        mock_exit.side_effect = SystemExit

        with (
            patch(
                "sys.argv", ["platzi-news", "search", "test", "--source", "guardian"]
            ),
            pytest.raises(SystemExit),
        ):
            await main()

        mock_exit.assert_called_once_with(1)


if __name__ == "__main__":
    pytest.main()
