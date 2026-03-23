# Contributing to Saudi Gov Navigator

العربية | [English](#english-section)

## المساهمة في مشروع دليل الخدمات الحكومية السعودية

شكراً لاهتمامك بالمساهمة في هذا المشروع! نرحب بجميع أشكال المساهمات من تحسينات الكود إلى تحديثات البيانات والتوثيق.

### أنواع المساهمات المرحب بها

#### 1. تحديثات البيانات (الأولوية العالية)
- **إضافة خدمات حكومية جديدة** إلى ملفات JSON
- **تحديث معلومات الخدمات الموجودة** بآخر التغييرات من المنصات الرسمية
- **إضافة متطلبات جديدة أو خطوات محدثة** للخدمات
- **تصحيح الأخطاء في البيانات الموجودة**

#### 2. تحسينات الكود
- إضافة ميزات جديدة للوكلاء أو محرك البحث
- تحسين الأداء والكفاءة
- إعادة هيكلة الكود لتحسين الوضوح والصيانة
- إضافة معالجة أفضل للأخطاء

#### 3. الاختبارات
- إضافة اختبارات وحدة جديدة
- تحسين تغطية الاختبارات
- اختبار السيناريوهات الواقعية

#### 4. التوثيق
- تحديث الوثائق الموجودة
- إضافة أمثلة جديدة
- ترجمة التوثيق إلى لغات أخرى
- تحسين وضوح الشرح

### بدء المساهمة

#### الخطوة 1: إعداد بيئة التطوير

```bash
# استنساخ المستودع
git clone https://github.com/yourusername/saudi-gov-navigator.git
cd saudi-gov-navigator

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# تثبيت المتطلبات
pip install -r requirements.txt
pip install -r requirements-dev.txt

# تثبيت في وضع التطوير
pip install -e .
```

#### الخطوة 2: إنشاء فرع للعمل

```bash
git checkout -b feature/your-feature-name
# أو للإصلاحات:
git checkout -b fix/your-fix-name
```

### معايير الكود

#### أسلوب البرمجة Python

1. **اتباع PEP 8**: استخدم معايير Python الرسمية
   ```bash
   # تحقق من الأسلوب
   flake8 saudi_gov/
   ```

2. **Type Hints**: استخدم تلميحات الأنواع في جميع الدوال
   ```python
   def get_service(service_id: str) -> Optional[Dict[str, Any]]:
       """احصل على خدمة حسب المعرف."""
       pass
   ```

3. **Docstrings**: اكتب docstrings واضحة لجميع الوحدات والفئات والدوال
   ```python
   def search_services(query: str, language: str = "ar") -> List[Dict]:
       """
       ابحث عن الخدمات حسب الاستعلام.

       Args:
           query: نص البحث
           language: اللغة ("ar" أو "en")

       Returns:
           قائمة بنتائج البحث
       """
       pass
   ```

#### المعايير الثنائية اللغة

جميع المتغيرات والدوال والتعليقات يجب أن تكون بالإنجليزية:

```python
# ✓ صحيح
def get_service_name_ar(service: Dict) -> str:
    """احصل على اسم الخدمة بالعربية."""
    return service.get("name_ar", "")

# ✗ خاطئ
def احصل_على_اسم_الخدمة(خدمة: Dict) -> str:
    """Get the service name in Arabic."""
    return خدمة.get("name_ar", "")
```

### معايير البيانات

#### هيكل خدمة JSON

كل خدمة يجب أن تتبع هذا الهيكل:

```json
{
  "id": "unique_service_id",
  "name_ar": "اسم الخدمة بالعربية",
  "name_en": "Service Name in English",
  "category": "فئة الخدمة",
  "category_en": "Category",
  "description_ar": "وصف مفصل للخدمة بالعربية",
  "description_en": "Detailed description in English",
  "requirements": ["متطلب 1", "متطلب 2"],
  "requirements_en": ["Requirement 1", "Requirement 2"],
  "steps": ["خطوة 1", "خطوة 2"],
  "steps_en": ["Step 1", "Step 2"],
  "fees": {
    "amount": 0,
    "currency": "SAR",
    "note": "ملاحظة عن الرسوم"
  },
  "fees_en": {
    "amount": 0,
    "currency": "SAR",
    "note": "Fee note"
  },
  "processing_time": "مدة المعالجة",
  "processing_time_en": "Processing Duration",
  "common_mistakes": ["خطأ شائع 1"],
  "common_mistakes_en": ["Common Mistake 1"],
  "tips": ["نصيحة 1"],
  "tips_en": ["Tip 1"],
  "eligibility": {
    "nationality": "السعودية وغيرها",
    "age_min": 0,
    "age_max": null,
    "requirements": "متطلبات الأهلية"
  }
}
```

#### التحقق من البيانات

- تأكد من اكتمال جميع الحقول المطلوبة
- تحقق من دقة المعلومات من مصادر رسمية
- استخدم الصيغة الصحيحة للعملة والتواريخ
- تحقق من التناسق بين النصوص العربية والإنجليزية

### الاختبار

#### تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
python -m pytest tests/

# تشغيل ملف اختبار معين
python -m pytest tests/test_knowledge_base.py

# مع تفاصيل التغطية
pytest --cov=saudi_gov tests/
```

#### كتابة اختبارات جديدة

```python
import unittest
from saudi_gov.agents.navigator_agent import NavigatorAgent

class TestNewFeature(unittest.TestCase):
    """اختبارات الميزة الجديدة."""

    def setUp(self):
        """إعداد الاختبار."""
        self.agent = NavigatorAgent(language="ar")

    def test_new_functionality(self):
        """اختبر الوظيفة الجديدة."""
        result = self.agent.some_method()
        self.assertIsNotNone(result)
        self.assertIn("expected_key", result)

if __name__ == "__main__":
    unittest.main()
```

**المتطلبات**:
- كل ميزة جديدة يجب أن تأتي مع اختبارات
- يجب أن تجتاز جميع الاختبارات الموجودة
- يجب أن تكون تغطية الاختبارات ≥ 80%

### عملية الإرسال

#### الخطوة 1: قم بالتغييرات المطلوبة

```bash
# قم بإجراء التغييرات الخاصة بك
git add .
git commit -m "الوصف القصير للتغيير"
```

#### الخطوة 2: رسائل الالتزام

استخدم رسائل التزام واضحة ومفيدة:

```
# ✓ صحيح
feat: إضافة خدمات استقدام العمالة إلى منصة قوى العمل
fix: إصلاح الخطأ في معالجة النصوص العربية
docs: تحديث وثائق الهندسة المعمارية
test: إضافة اختبارات لوحدة البحث الدلالي

# ✗ خاطئ
updated code
fix stuff
added things
```

#### الخطوة 3: إرسال طلب الدمج (PR)

1. ادفع فرعك إلى مستودعك على GitHub
2. افتح Pull Request إلى الفرع الرئيسي
3. ملأ قالب PR بالمعلومات المطلوبة:

**قالب طلب الدمج:**
```markdown
## الوصف
وصف موجز لما يفعله هذا PR

## نوع التغيير
- [ ] إضافة ميزة جديدة
- [ ] إصلاح خطأ
- [ ] تحديث التوثيق
- [ ] تحسين الأداء
- [ ] تحديث البيانات

## الاختبار
- [ ] اختبرت التغييرات محلياً
- [ ] اجتازت جميع الاختبارات الموجودة
- [ ] أضفت اختبارات جديدة (إن كان ضروريًا)

## قائمة المراجعة
- [ ] اتبعت معايير الكود
- [ ] أضفت/حدثت التوثيق
- [ ] الرسائل واضحة والتزامات منظمة
```

### إرشادات المراجعة

عند مراجعة PRs أخرى:

1. **تحقق من جودة الكود**
   - هل يتبع معايير PEP 8؟
   - هل تحتوي الدوال على type hints و docstrings؟
   - هل الكود واضح وسهل الفهم؟

2. **تحقق من البيانات**
   - هل المعلومات دقيقة من مصادر رسمية؟
   - هل متوازنة بين العربية والإنجليزية؟
   - هل اتبعت معايير JSON؟

3. **تحقق من الاختبارات**
   - هل يتم اختبار الحالات الإيجابية والسلبية؟
   - هل التغطية كافية؟

4. **كن محترماً وبناء**
   - ركز على الكود وليس على الشخص
   - اقترح تحسينات وليس انتقادات فقط
   - اشكر المساهم على مجهوده

### الاتصال والمساعدة

- **المشاكل والأسئلة**: استخدم GitHub Issues
- **النقاشات**: استخدم GitHub Discussions
- **البريد الإلكتروني**: [يمكن إضافة بريد تواصل]

### قواعس السلوك

نتوقع من جميع المساهمين:

- احترام جميع المساهمين الآخرين
- عدم التمييز على أساس العرق أو الجنس أو الدين أو الجنسية
- عدم الإساءة اللفظية أو السلوك المسيء
- قبول النقد البناء بصدر رحب

انتهاكات قواعس السلوك قد تؤدي لحظر من المشروع.

### الترخيص

بالمساهمة في هذا المشروع، فإنك توافق على أن تكون مساهماتك تحت رخصة MIT. للمزيد من المعلومات، انظر ملف LICENSE.

---

<a name="english-section"></a>

# Contributing to Saudi Gov Navigator

Thank you for your interest in contributing to this project! We welcome all forms of contributions from code improvements to data updates and documentation.

### Welcome Contribution Types

#### 1. Data Updates (High Priority)
- **Add new government services** to JSON files
- **Update existing service information** with latest changes from official platforms
- **Add new requirements or updated steps** for services
- **Correct errors in existing data**

#### 2. Code Improvements
- Add new features to agents or search engine
- Improve performance and efficiency
- Refactor code for better clarity and maintainability
- Improve error handling

#### 3. Tests
- Add new unit tests
- Improve test coverage
- Test real-world scenarios

#### 4. Documentation
- Update existing documentation
- Add new examples
- Translate documentation to other languages
- Improve clarity of explanations

### Getting Started

#### Step 1: Set Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/saudi-gov-navigator.git
cd saudi-gov-navigator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

#### Step 2: Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# Or for fixes:
git checkout -b fix/your-fix-name
```

### Code Standards

#### Python Style Guidelines

1. **Follow PEP 8**: Use official Python standards
   ```bash
   # Check style
   flake8 saudi_gov/
   ```

2. **Type Hints**: Use type hints in all functions
   ```python
   def get_service(service_id: str) -> Optional[Dict[str, Any]]:
       """Get service by ID."""
       pass
   ```

3. **Docstrings**: Write clear docstrings for all modules, classes, and functions
   ```python
   def search_services(query: str, language: str = "ar") -> List[Dict]:
       """
       Search for services by query.

       Args:
           query: Search text
           language: Language ("ar" or "en")

       Returns:
           List of search results
       """
       pass
   ```

#### Bilingual Standards

All variables, functions, and code comments must be in English:

```python
# ✓ Correct
def get_service_name_ar(service: Dict) -> str:
    """احصل على اسم الخدمة بالعربية."""
    return service.get("name_ar", "")

# ✗ Incorrect
def احصل_على_اسم_الخدمة(خدمة: Dict) -> str:
    """Get the service name in Arabic."""
    return خدمة.get("name_ar", "")
```

### Data Standards

#### Service JSON Structure

Each service must follow this structure:

```json
{
  "id": "unique_service_id",
  "name_ar": "اسم الخدمة بالعربية",
  "name_en": "Service Name in English",
  "category": "فئة الخدمة",
  "category_en": "Category",
  "description_ar": "وصف مفصل للخدمة بالعربية",
  "description_en": "Detailed description in English",
  "requirements": ["متطلب 1", "متطلب 2"],
  "requirements_en": ["Requirement 1", "Requirement 2"],
  "steps": ["خطوة 1", "خطوة 2"],
  "steps_en": ["Step 1", "Step 2"],
  "fees": {
    "amount": 0,
    "currency": "SAR",
    "note": "ملاحظة عن الرسوم"
  },
  "fees_en": {
    "amount": 0,
    "currency": "SAR",
    "note": "Fee note"
  },
  "processing_time": "مدة المعالجة",
  "processing_time_en": "Processing Duration",
  "common_mistakes": ["خطأ شائع 1"],
  "common_mistakes_en": ["Common Mistake 1"],
  "tips": ["نصيحة 1"],
  "tips_en": ["Tip 1"],
  "eligibility": {
    "nationality": "السعودية وغيرها",
    "age_min": 0,
    "age_max": null,
    "requirements": "متطلبات الأهلية"
  }
}
```

#### Data Validation

- Ensure all required fields are complete
- Verify information accuracy from official sources
- Use correct format for currency and dates
- Check consistency between Arabic and English text

### Testing

#### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_knowledge_base.py

# With coverage details
pytest --cov=saudi_gov tests/
```

#### Writing New Tests

```python
import unittest
from saudi_gov.agents.navigator_agent import NavigatorAgent

class TestNewFeature(unittest.TestCase):
    """Tests for new feature."""

    def setUp(self):
        """Set up test."""
        self.agent = NavigatorAgent(language="ar")

    def test_new_functionality(self):
        """Test the new functionality."""
        result = self.agent.some_method()
        self.assertIsNotNone(result)
        self.assertIn("expected_key", result)

if __name__ == "__main__":
    unittest.main()
```

**Requirements**:
- Every new feature must come with tests
- All existing tests must pass
- Test coverage should be ≥ 80%

### Submission Process

#### Step 1: Make Your Changes

```bash
# Make your changes
git add .
git commit -m "Brief description of change"
```

#### Step 2: Commit Messages

Use clear and helpful commit messages:

```
# ✓ Correct
feat: add worker recruitment services to labor platform
fix: correct Arabic text processing bug
docs: update architecture documentation
test: add tests for semantic search module

# ✗ Incorrect
updated code
fix stuff
added things
```

#### Step 3: Submit Pull Request

1. Push your branch to your GitHub fork
2. Open a Pull Request to the main branch
3. Fill in the PR template with required information:

**Pull Request Template:**
```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Data update

## Testing
- [ ] Tested changes locally
- [ ] All existing tests pass
- [ ] Added new tests (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Added/updated documentation
- [ ] Messages are clear and commits organized
```

### Review Guidelines

When reviewing other PRs:

1. **Check Code Quality**
   - Does it follow PEP 8?
   - Do functions have type hints and docstrings?
   - Is the code clear and understandable?

2. **Check Data**
   - Is information accurate from official sources?
   - Is balance maintained between Arabic and English?
   - Does it follow JSON standards?

3. **Check Tests**
   - Are positive and negative cases tested?
   - Is coverage sufficient?

4. **Be Respectful and Constructive**
   - Focus on code, not person
   - Suggest improvements, not just criticisms
   - Thank the contributor for their effort

### Communication and Help

- **Issues and Questions**: Use GitHub Issues
- **Discussions**: Use GitHub Discussions
- **Email**: [can add contact email]

### Code of Conduct

We expect all contributors to:

- Respect all other contributors
- Avoid discrimination based on race, gender, religion, or nationality
- Avoid verbal abuse or offensive behavior
- Accept constructive criticism gracefully

Violations of the code of conduct may result in banning from the project.

### License

By contributing to this project, you agree that your contributions will be under the MIT License. For more information, see the LICENSE file.
