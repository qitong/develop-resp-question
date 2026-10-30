# 呼吸科选题数据库地图

按“回答选题中的哪个问题”组织。✅ = 公开 API；🌐 = 网页检索；🔑 = 注册、申请或授权。`scripts/resp_scan.py` 已接入 PubMed、Europe PMC 和 ClinicalTrials.gov。**指南、会议和数据库会更新，引用前核对当前版本、发布日期与原文。**

## 目录

1. 已知什么：文献、系统评价与会议
2. 谁在做：注册平台与竞争格局
3. 标准是什么：指南与监管
4. 生物学、组学与公共数据
5. 影像、生理与真实世界数据
6. 流行病学与可行性
7. API 速查
8. 跨领域借鉴

## 1. 已知什么？（文献与会议）

| 数据源 | 用途 | 访问 |
|---|---|---|
| PubMed / MEDLINE | 主文献库；MeSH + 自由词 + 研究类型 | ✅ E-utilities `esearch/esummary/efetch` |
| Europe PMC | 全文、引用、预印本 | ✅ REST search |
| Cochrane Library | 已有系统评价，避免重复 | 🌐 |
| OpenAlex | 引用网络、作者/机构与批评者 | ✅ 无 key 额度有限 |
| ERS International Congress | ILD、COPD、哮喘、感染、肺血管等最新摘要 | 🌐 |
| ATS International Conference | 呼吸与危重症最新摘要 | 🌐 |
| CHEST Annual Meeting | 临床呼吸、ILD、重症、介入 | 🌐 |
| EULAR / ACR Convergence | CTD-ILD、SSc、RA、IIM、SjD 等风湿交叉证据 | 🌐 |
| 中华医学会呼吸病学年会等 | 中国人群、本土实践与单中心研究 | 🌐 |
| 中国知网 / 万方 / 中华医学期刊网 | 中文文献与本土队列 | 🌐 |

PubMed 实用检索块：
- 疾病：`"Pulmonary Fibrosis"[Mesh]`、`"Lung Diseases, Interstitial"[Mesh]`、`"Connective Tissue Diseases"[Mesh]`
- PPF 自由词：`"progressive pulmonary fibrosis" OR "progressive fibrosing interstitial lung disease" OR "progressive fibrosing ILD"`
- CTD-ILD：`("connective tissue disease" OR systemic sclerosis OR rheumatoid arthritis OR idiopathic inflammatory myopathy OR Sjogren*) AND ("interstitial lung disease" OR ILD)`
- RCT：`randomized controlled trial[pt]`
- 真实世界：`(real-world OR "real world" OR retrospective OR registry OR cohort)`
- 中国人群：`(China[ad] OR Chinese[tiab] OR China[tiab])`

检索时并列旧术语和新术语；不要只用 PPF 缩写，因为它还可能指其他概念。

## 2. 谁在做？（注册与撞车检查）

| 数据源 | 用途 | 访问 |
|---|---|---|
| ClinicalTrials.gov | 全球注册、状态、终点、入排、样本量 | ✅ API v2 |
| ChiCTR | 国内 IIT、队列和干预研究 | 🌐 https://www.chictr.org.cn/ |
| WHO ICTRP | 多国注册平台汇总 | 🌐 https://trialsearch.who.int/ |
| CDE 药物临床试验登记平台 | 国内注册类药物试验 | 🌐 http://www.chinadrugtrials.org.cn/ |
| EU CTIS | 欧洲试验 | 🌐 |
| jRCT / JPRN、ISRCTN、ANZCTR | 地区性研究补充 | 🌐 |

撞车检查要比较：疾病定义、治疗线/背景治疗、T0、主要终点、样本量、预计完成时间。相同药名不等于相同问题；相同病名也不等于可比较人群。

## 3. 标准是什么？（指南与监管）

| 领域 | 主要来源 | 选题用法 |
|---|---|---|
| IPF / PPF | ATS/ERS/JRS/ALAT 指南及更新 | 诊断路径、PPF 定义、抗纤维化推荐与证据质量 |
| CTD-ILD / SARD-ILD | ERS/EULAR、ACR/CHEST；各 CTD 专病指南 | 筛查、MDD、免疫抑制与抗纤维化定位、监测间隔 |
| ILD 综合 | ATS/ERS、BTS、CHEST、国家/地区 ILD 指南或共识 | 分类、AE-ILD、康复、氧疗、移植与姑息 |
| COPD | GOLD 报告、ATS/ERS、中国指南 | 可干预特质、急性加重、吸入治疗、康复 |
| 哮喘 | GINA、ERS/ATS、中国指南 | 重度哮喘表型、生物制剂、可干预危险因素 |
| 肺部感染 | IDSA/ATS、ERS、WHO、国家指南 | 病原、疗程、耐药、宿主与重症 |
| 肺高压 / 肺血管 | ESC/ERS、CHEST | 分类、风险分层、CTD/ILD 相关肺高压 |
| 睡眠呼吸障碍 | AASM、ERS、ATS | 诊断、PAP 依从性、合并症 |
| 介入 / 胸膜 / 呼吸重症 | CHEST、ATS/ERS、 SCCM、专业学会 | 技术比较、并发症、患者选择与结局 |

监管补充：FDA/openFDA、EMA、NMPA/CDE 用于核对适应症边界、说明书和上市后要求。指南中的弱推荐或低质量证据是候选空白，不等于必然值得做；需判断空白是否来自证据难做、临床不重要，还是已有新证据未纳入。

## 4. 生物学、组学与公共数据

| 数据源 | 用途 | 访问 |
|---|---|---|
| GEO / SRA | 表达谱、单细胞、机制数据与验证队列 | ✅ NCBI |
| LungMAP | 肺发育与肺细胞图谱 | 🌐 / 下载 |
| IPF Cell Atlas | IPF 单细胞与相关数据资源 | 🌐 / 下载，核对当前数据集 |
| CELLxGENE | 肺组织与疾病单细胞数据 | ✅ / 🌐 |
| GTEx | 正常肺组织表达与 eQTL | 🌐 / 🔑 部分数据 |
| Human Protein Atlas | 正常/疾病组织蛋白表达 | 🌐 |
| Open Targets | 基因/靶点—疾病关联与药物证据 | ✅ GraphQL |
| GWAS Catalog | IPF、肺功能、COPD、哮喘等遗传关联 | ✅ / 🌐 |
| FinnGen / UK Biobank | 遗传与临床结局；肺功能、ILD 等表型 | 🔑 / 按开放程度 |
| ENCODE / Roadmap | 调控元件与功能注释 | 🌐 / 下载 |

提醒：公共组学数据常有中心、平台、组织区域、病程与治疗批次；病例数小、重复样本和供体差异要进入设计。发现队列与验证队列不能来自同一批次简单拆分后就宣称“外部验证”。

## 5. 影像、生理与真实世界数据

| 数据源 | 用途 | 访问 |
|---|---|---|
| OSIC（Open Source Imaging Consortium） | ILD/肺纤维化影像与相关数据 | 🌐 / 🔑 按数据协议 |
| TCIA | 公开影像集合；先确认是否含目标 ILD 与临床结局 | 🌐 / 下载 |
| PhysioNet | 睡眠、呼吸波形、重症生理数据 | 🌐 / 🔑 按数据集 |
| MIMIC-IV / eICU | 呼吸重症、机械通气、临床结局 | 🔑 培训与数据协议 |
| 公开 ILD 登记与队列 | 自然史、进展、治疗与预后；先确认申请条件 | 🌐 / 🔑 |
| 本院 HIS / EMR | 诊断、用药、感染、住院与结局 | 本地 / 伦理 |
| PFT 系统 | FVC、DLCO、质控、预计值与检查时间 | 本地 |
| PACS / 影像后处理 | HRCT 图像、扫描参数、定量纤维化/肺气肿 | 本地 |
| 风湿/ILD 专病库与 MDD 记录 | CTD 分型、抗体、诊断置信度与重分类 | 本地 |

关键核对：同一患者多次检查是否可比；PFT 是否符合质控、预计值公式是否一致；HRCT 层厚/重建/吸气程度是否一致；DLCO 是否校正血红蛋白；6MWD 是否统一吸氧与流程；数据库中“诊断编码”是否经 MDD 或病历复核。

## 6. 做得出来吗？（流行病学与可行性）

| 数据源 | 用途 | 访问 |
|---|---|---|
| GBD / IHME | 呼吸疾病负担与趋势；注意 ILD 细分能力有限 | 🌐 |
| 国家/地区呼吸疾病调查 | COPD、哮喘等人群患病率与危险因素 | 🌐 |
| 文献中的登记队列 | 事件率、失访、治疗格局和入组速度参照 | 🌐 |
| 本院连续病例筛查 | 真正决定可行性的病例流与数据完整度 | 本地 |
| 检验/微生物/病理/输血等系统 | 暴露、合并症和结局补充 | 本地 |

入组粗估：`年就诊量 × 诊断符合率 × 目标表型比例 × 入排通过率 × 同意率 × 完整随访率`。

回顾性可行性至少抽查 30–50 份连续病历，列出：诊断可确认率、目标检查可得率、检查间隔、关键变量缺失率、随访完整率、事件数。模型样本量由参数/事件数与预期性能决定，不用“总病例数很多”代替。

## 7. API 速查

```bash
# PubMed：PPF 文献数
curl -sG "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" \
  --data-urlencode 'db=pubmed' --data-urlencode 'retmode=json' \
  --data-urlencode 'term="progressive pulmonary fibrosis"'

# Europe PMC：CTD-ILD 预印本
curl -sG "https://www.ebi.ac.uk/europepmc/webservices/rest/search" \
  --data-urlencode 'query=("connective tissue disease" AND "interstitial lung disease") AND SRC:PPR' \
  --data-urlencode 'format=json'

# ClinicalTrials.gov：PPF + 干预
curl -sG "https://clinicaltrials.gov/api/v2/studies" \
  --data-urlencode 'query.cond=progressive pulmonary fibrosis' \
  --data-urlencode 'query.intr=nintedanib' --data-urlencode 'countTotal=true'

# GEO：ILD 数据集
curl -sG "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" \
  --data-urlencode 'db=gds' --data-urlencode 'retmode=json' \
  --data-urlencode 'term=interstitial lung disease'

# openFDA：药品说明书
curl -sG "https://api.fda.gov/drug/label.json" \
  --data-urlencode 'search=openfda.generic_name:nintedanib' --data-urlencode 'limit=1'
```

## 8. 跨领域借鉴

- **ILD 内部**：IPF 的自然史与抗纤维化经验能否迁移到非 IPF PPF？哪些部分受 CTD 免疫机制限制？
- **风湿—呼吸**：SSc-ILD 的筛查和监测策略能否用于 RA/IIM/SjD？抗体、皮肤/肌肉活动和肺进展是否同步？
- **慢病管理**：COPD/心衰的家庭监测、康复、急性加重路径能否转化为 ILD 的可执行干预，而不只是预测模型？
- **方法学**：目标试验模拟、重复测量轨迹、竞争风险、多状态模型、因果机器学习、定量 HRCT、数字 PRO。
- **临床动作优先**：任何新表型、评分或模型都要回答“谁在何时因此改变什么处理，患者得到什么额外获益”。
