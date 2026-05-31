# PowerShell COM 生成 Word 文档通用模板
# 本机需安装 Microsoft Office

# 参数设置
$OutputPath = "$PSScript_ROOT\output.docx"

# 启动 Word 应用程序
$Word = New-Object -ComObject Word.Application
$Word.Visible = $false  # 设为 $true 可见 Word 窗口（调试用）

# 创建新文档
$Doc = $Word.Documents.Add()

# ----- 写入内容 -----
# 写入文本
$Paragraph = $Doc.Content.Paragraphs.Add()
$Paragraph.Range.Text = "标题文字"
$Paragraph.Range.Bold = 1
$Paragraph.Range.Font.Size = 18
$Paragraph.Range.Font.Name = "SimSun"
$Paragraph.Range.InsertParagraphAfter()

# 写入正文
$Paragraph = $Doc.Content.Paragraphs.Add()
$Paragraph.Range.Text = "正文内容"
$Paragraph.Range.Font.Size = 12
$Paragraph.Range.Font.Name = "SimSun"
$Paragraph.Range.InsertParagraphAfter()

# 换行
$Doc.Content.Paragraphs.Add() | Out-Null

# 写入表格
$Table = $Doc.Tables.Add($Doc.Range($Doc.Content.End - 1), 3, 3)
$Table.Cell(1,1).Range.Text = "表头1"
$Table.Cell(1,2).Range.Text = "表头2"
$Table.Cell(1,3).Range.Text = "表头3"
$Table.Cell(2,1).Range.Text = "数据A"
$Table.Cell(2,2).Range.Text = "数据B"
$Table.Cell(2,3).Range.Text = "数据C"
# 设置表格样式
$Table.Style = "Light Grid Accent 1"

# 分页
$Doc.Content.Paragraphs.Add() | Out-Null
$Doc.Content.Paragraphs.Add() | Out-Null  # 分页前加空行
$Selection = $Word.Selection
$Selection.InsertBreak(7)  # 7 = wdPageBreak

# 新的一页
$Paragraph = $Doc.Content.Paragraphs.Add()
$Paragraph.Range.Text = "第二页内容"
$Paragraph.Range.Font.Size = 12
$Paragraph.Range.InsertParagraphAfter()

# ----- 保存并退出 -----
$Doc.SaveAs([System.IO.Path]::GetFullPath($OutputPath))
$Word.Quit()

# 释放 COM 对象
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($Doc) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($Word) | Out-Null
Remove-Variable Doc, Word

Write-Host "已生成: $OutputPath"
