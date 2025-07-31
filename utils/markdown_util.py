from typing import List, Dict, Any, Optional


class MarkdownUtil:
    """
    一个Markdown文本处理工具

    Markdown表格处理:
    1. data as list of dicts:
       data = [{"Name": "Alice", "Age": 25}, {"Name": "Bob", "Age": 30}]
       MarkdownUtil.from_dicts(data)

    2. data as list of rows with headers:
       headers = ["Name", "Age"]
       data = [["Alice", 25], ["Bob", 30]]
       MarkdownUtil.from_rows(headers, data)

    3. custom alignment:
       MarkdownUtil.from_rows(headers, data, align=["left", "right"])
    """

    @classmethod
    def from_dicts(
            cls,
            data: List[Dict[str, Any]],
            align: str = "left",
    ) -> str:
        """
        基于列表字典的数据生成Markdown表格
        Args:
            data: 数据源
            align: 列表对齐方式,默认left

        Returns:
            Markdown表格Str
        """
        if not data:
            return ""

        headers = list(data[0].keys())
        rows = [[row.get(col, "") for col in headers] for row in data]
        return cls._build_table(headers, rows, align)

    @classmethod
    def from_rows(
            cls,
            headers: List[str],
            data: List[List[Any]],
            align: str = "left"
    ) -> str:
        """
        基于指定列表头和指定数据生成Markdown表格
        Args:
            headers: 列表头
            data: 数据源
            align: 列表对齐方式,默认left

        Returns:
            Markdown表格Str
        """
        if not headers:
            return ""
        rows = data if data else []
        return cls._build_table(headers, rows, align)

    @classmethod
    def _build_table(
            cls,
            headers: List[str],
            rows: List[List[Any]],
            align: str
    ) -> str:
        """
        核心处理方法
        """
        align_val = cls._normalize_align(align)
        # 构建表头行
        header_row = cls._format_row(headers)
        # 构建对齐行
        align_row = cls._format_align_row(len(headers), align_val)
        # 构建数据行
        data_rows = [cls._format_row([str(cell) for cell in row]) for row in rows]

        table = [header_row, align_row] + data_rows
        return "\n".join(table)

    @classmethod
    def _normalize_align(
            cls,
            align: str
    ) -> str:
        """
        验证并返回对齐方式
        """
        valid = {"left", "center", "right"}
        if align not in valid:
            raise ValueError(
                f"无效的对齐方式 '{align}'，可选: 'left', 'center', 'right'"
            )
        return align

    @classmethod
    def _format_row(cls, items: List[str]) -> str:
        """
        将一行数据格式化为Markdown表格行
        """
        return "| " + " | ".join(items) + " |"

    @classmethod
    def _format_align_row(cls, count: int, align: str) -> str:
        """
        根据对齐方式生成对齐行
        """
        if align == "left":
            cell = ":---"
        elif align == "center":
            cell = ":---:"
        else:  # right
            cell = "---:"
        return "| " + " | ".join([cell] * count) + " |"


if __name__ == "__main__":
    print(MarkdownUtil.from_dicts([
        {"Name": "Alice", "Age": 25},
    ]))
    print(MarkdownUtil.from_rows(headers=["Name", "Age"],
                                 data=[["Alice", 25], ["Bob", 30]]))
