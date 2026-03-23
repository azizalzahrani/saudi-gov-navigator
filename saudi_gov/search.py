"""
Search Module - وحدة البحث

Semantic search functionality for finding government services.
وظائف البحث الدلالي للعثور على الخدمات الحكومية.
"""

import re
from typing import List, Dict, Any
from saudi_gov.knowledge_base import load_all_services
from saudi_gov.utils.arabic_utils import normalize_arabic_text

ARABIC_STOP_WORDS = {
    "ما",
    "ماذا",
    "كيف",
    "هل",
    "انا",
    "أنا",
    "اريد",
    "أريد",
    "ابي",
    "أبي",
    "ابغى",
    "أبغى",
    "في",
    "من",
    "على",
    "عن",
    "إلى",
    "الى",
    "مع",
    "ثم",
    "هذه",
    "هذا",
    "هناك",
    "التي",
    "الذي",
    "الخطوات",
    "الخطوات",
    "عندي",
}

ENGLISH_STOP_WORDS = {
    "the",
    "a",
    "an",
    "how",
    "what",
    "i",
    "me",
    "my",
    "for",
    "to",
    "in",
    "on",
    "of",
    "and",
    "with",
}


class SemanticSearch:
    """
    Semantic search engine for finding government services.

    محرك البحث الدلالي للعثور على الخدمات الحكومية.
    """

    def __init__(self, language: str = "ar"):
        """
        Initialize the semantic search engine.

        Parameters:
            language: Language for search ("ar" for Arabic, "en" for English)
        """
        self.language = language
        self.services = load_all_services()
        self._build_search_index()

    def _build_search_index(self) -> None:
        """Build an index of all services for faster searching."""
        self.search_index = []

        for platform_name, platform_data in self.services.items():
            services = platform_data.get("services", [])
            for service in services:
                searchable_text = self._create_searchable_text(
                    service=service,
                    platform_name=platform_name,
                    platform_data=platform_data,
                )
                indexed_item = {
                    "service_id": service.get("id"),
                    "platform": platform_name,
                    "service": service,
                    "searchable_text": searchable_text,
                    "platform_text": self._normalize_text(
                        " ".join(
                            filter(
                                None,
                                [
                                    platform_name,
                                    platform_data.get("platform_en", ""),
                                    platform_data.get("platform_ar", ""),
                                ],
                            )
                        )
                    ),
                    "name_text": self._normalize_text(
                        " ".join(
                            filter(
                                None,
                                [
                                    service.get("name_ar", ""),
                                    service.get("name_en", ""),
                                ],
                            )
                        )
                    ),
                    "description_text": self._normalize_text(
                        " ".join(
                            filter(
                                None,
                                [
                                    service.get("description_ar", ""),
                                    service.get("description_en", ""),
                                ],
                            )
                        )
                    ),
                }
                self.search_index.append(indexed_item)

    def _create_searchable_text(
        self,
        service: Dict[str, Any],
        platform_name: str,
        platform_data: Dict[str, Any],
    ) -> str:
        """Create concatenated searchable text from service fields."""
        eligibility = service.get("eligibility", {})
        text_parts = [
            service.get("id", ""),
            service.get("name_ar", ""),
            service.get("name_en", ""),
            service.get("description_ar", ""),
            service.get("description_en", ""),
            service.get("category", ""),
            service.get("category_en", ""),
            platform_name,
            platform_data.get("platform_ar", ""),
            platform_data.get("platform_en", ""),
            " ".join(service.get("requirements", [])),
            " ".join(service.get("requirements_en", [])),
            " ".join(service.get("steps", [])),
            " ".join(service.get("steps_en", [])),
            " ".join(service.get("tips", [])),
            " ".join(service.get("tips_en", [])),
            " ".join(
                str(value) for value in eligibility.values() if value is not None
            ),
        ]
        return self._normalize_text(" ".join(text_parts))

    def _normalize_text(self, text: str) -> str:
        """Normalize text for Arabic/English keyword matching."""
        if not text:
            return ""

        normalized = normalize_arabic_text(text)
        normalized = (
            normalized.replace("أ", "ا")
            .replace("إ", "ا")
            .replace("آ", "ا")
            .replace("ؤ", "و")
            .replace("ئ", "ي")
        )
        normalized = normalized.lower()
        normalized = normalized.translate(
            str.maketrans({
                "؟": " ",
                "،": " ",
                "؛": " ",
                "ـ": "",
            })
        )
        normalized = re.sub(r"[^0-9a-z\u0621-\u064a\s]", " ", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def _extract_query_terms(self, query: str) -> List[str]:
        """Extract useful query terms after removing filler words."""
        normalized = self._normalize_text(query)
        tokens = re.findall(r"[0-9a-z\u0621-\u064a]+", normalized)

        terms = []
        seen = set()
        stop_words = ARABIC_STOP_WORDS | ENGLISH_STOP_WORDS
        for token in tokens:
            if token in stop_words or len(token) <= 1:
                continue
            if token not in seen:
                terms.append(token)
                seen.add(token)
        return terms

    def _token_variants(self, token: str) -> List[str]:
        """Generate simple Arabic/English variants for better recall."""
        variants = {token}

        if token.startswith("ال") and len(token) > 4:
            variants.add(token[2:])

        if token.startswith("ا") and len(token) > 3:
            variants.add(token[1:])

        for suffix in ("يات", "ات", "ون", "ين", "ان", "ية", "ه", "ها", "هم", "كم", "نا", "ي", "ك", "ة"):
            if token.endswith(suffix) and len(token) > len(suffix) + 2:
                variants.add(token[:-len(suffix)])

        return sorted(variant for variant in variants if variant)

    def _count_term_matches(self, terms: List[str], target_text: str) -> int:
        """Count how many query terms match a target string."""
        matches = 0
        for term in terms:
            variants = self._token_variants(term)
            if any(variant in target_text for variant in variants):
                matches += 1
        return matches

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for services using keyword matching.

        البحث عن الخدمات باستخدام مطابقة الكلمات الرئيسية.

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            List of matching services with relevance scores
        """
        if not query or not query.strip():
            return []

        query_lower = self._normalize_text(query)
        query_terms = self._extract_query_terms(query)

        results_with_scores = []

        for indexed_item in self.search_index:
            service = indexed_item["service"]
            searchable_text = indexed_item["searchable_text"]

            # Calculate relevance score
            score = self._calculate_relevance_score(
                query_lower=query_lower,
                query_terms=query_terms,
                service=service,
                searchable_text=searchable_text,
                name_text=indexed_item["name_text"],
                description_text=indexed_item["description_text"],
                platform_text=indexed_item["platform_text"],
            )

            if score > 0:
                results_with_scores.append({
                    "service": service,
                    "platform": indexed_item["platform"],
                    "score": score,
                })

        # Sort by score (descending) and return top results
        results_with_scores.sort(key=lambda x: x["score"], reverse=True)
        return results_with_scores[:max_results]

    def _calculate_relevance_score(
        self,
        query_lower: str,
        query_terms: List[str],
        service: Dict[str, Any],
        searchable_text: str,
        name_text: str,
        description_text: str,
        platform_text: str,
    ) -> float:
        """Calculate relevance score for a service against query."""
        score = 0.0

        # Exact match in name (highest priority)
        name_ar = self._normalize_text(service.get("name_ar", ""))
        name_en = self._normalize_text(service.get("name_en", ""))

        if query_lower == name_ar or query_lower == name_en:
            score += 10.0

        # Partial match in name (high priority)
        if query_lower in name_text:
            score += 6.0

        # Match in description
        if query_lower in description_text:
            score += 3.0

        # Keyword matching with light Arabic normalization and suffix handling
        name_matches = self._count_term_matches(query_terms, name_text)
        searchable_matches = self._count_term_matches(query_terms, searchable_text)
        platform_matches = self._count_term_matches(query_terms, platform_text)

        score += name_matches * 2.5
        score += max(searchable_matches - name_matches, 0) * 1.0
        score += platform_matches * 1.5

        if query_terms and name_matches == len(query_terms):
            score += 4.0
        elif query_terms and searchable_matches == len(query_terms):
            score += 2.0

        return score

    def autocomplete(self, partial_query: str, max_suggestions: int = 5) -> List[str]:
        """
        Provide autocomplete suggestions for partial queries.

        توفير اقتراحات الإكمال التلقائي للاستفسارات الجزئية.

        Args:
            partial_query: Partial query string
            max_suggestions: Maximum suggestions to return

        Returns:
            List of suggested complete queries
        """
        suggestions = set()
        partial_lower = partial_query.lower()

        for indexed_item in self.search_index:
            service = indexed_item["service"]
            name_ar = service.get("name_ar", "")
            name_en = service.get("name_en", "")
            desc_ar = service.get("description_ar", "")
            desc_en = service.get("description_en", "")

            if partial_lower in name_ar.lower():
                suggestions.add(name_ar)
            if partial_lower in name_en.lower():
                suggestions.add(name_en)
            if partial_lower in desc_ar.lower():
                first_words = " ".join(desc_ar.split()[:3])
                suggestions.add(first_words)
            if partial_lower in desc_en.lower():
                first_words = " ".join(desc_en.split()[:3])
                suggestions.add(first_words)

        return list(suggestions)[:max_suggestions]

    def filter_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Filter services by category.

        تصفية الخدمات حسب الفئة.

        Args:
            category: Category name

        Returns:
            List of services in the category
        """
        results = []
        category_lower = category.lower()

        for indexed_item in self.search_index:
            service = indexed_item["service"]
            service_category = service.get("category", "").lower()
            service_category_en = service.get("category_en", "").lower()

            if category_lower in service_category or category_lower in service_category_en:
                results.append({
                    "service": service,
                    "platform": indexed_item["platform"],
                })

        return results

    def filter_by_platform(self, platform: str) -> List[Dict[str, Any]]:
        """
        Filter services by platform.

        تصفية الخدمات حسب المنصة.

        Args:
            platform: Platform name (Arabic)

        Returns:
            List of services from the platform
        """
        results = []
        platform_lower = platform.lower()

        for indexed_item in self.search_index:
            if platform_lower in indexed_item["platform"].lower():
                results.append({
                    "service": indexed_item["service"],
                    "platform": indexed_item["platform"],
                })

        return results

    def filter_by_fee(self, max_fee: float = 0.0) -> List[Dict[str, Any]]:
        """
        Filter services by fee amount.

        تصفية الخدمات حسب الرسوم.

        Args:
            max_fee: Maximum fee amount (0 for free services)

        Returns:
            List of services matching fee criteria
        """
        results = []

        for indexed_item in self.search_index:
            service = indexed_item["service"]
            fee_ar = service.get("fees", {}).get("amount", 0)
            fee_en = service.get("fees_en", {}).get("amount", 0)

            # Handle string amounts like "متغيرة" or "Varies"
            if isinstance(fee_ar, (int, float)) and fee_ar <= max_fee:
                results.append({
                    "service": service,
                    "platform": indexed_item["platform"],
                })
            elif isinstance(fee_en, (int, float)) and fee_en <= max_fee:
                results.append({
                    "service": service,
                    "platform": indexed_item["platform"],
                })

        return results

    def advanced_search(
        self,
        query: str = "",
        category: str = "",
        platform: str = "",
        max_fee: float = float("inf"),
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform advanced search with multiple filters.

        إجراء بحث متقدم بعدة مرشحات.

        Args:
            query: Text search query
            category: Category filter
            platform: Platform filter
            max_fee: Maximum fee filter
            max_results: Maximum results to return

        Returns:
            Filtered and ranked list of services
        """
        # Start with text search if query provided
        if query:
            results = self.search(query, max_results=100)
            result_set = {r["service"].get("id"): r for r in results}
        else:
            result_set = {
                indexed_item["service"].get("id"): {
                    "service": indexed_item["service"],
                    "platform": indexed_item["platform"],
                    "score": 1.0,
                } for indexed_item in self.search_index
            }

        # Apply category filter
        if category:
            category_results = self.filter_by_category(category)
            category_ids = {r["service"].get("id") for r in category_results}
            result_set = {
                k: v for k, v in result_set.items() if k in category_ids
            }

        # Apply platform filter
        if platform:
            platform_results = self.filter_by_platform(platform)
            platform_ids = {r["service"].get("id") for r in platform_results}
            result_set = {
                k: v for k, v in result_set.items() if k in platform_ids
            }

        # Apply fee filter
        if max_fee != float("inf"):
            fee_results = self.filter_by_fee(max_fee)
            fee_ids = {r["service"].get("id") for r in fee_results}
            result_set = {
                k: v for k, v in result_set.items() if k in fee_ids
            }

        # Sort by score and return top results
        sorted_results = sorted(
            result_set.values(),
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        return sorted_results[:max_results]

    def get_related_services(
        self, service_id: str, max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find services related to a given service.

        البحث عن الخدمات ذات الصلة بخدمة معينة.

        Args:
            service_id: Reference service ID
            max_results: Maximum related services to return

        Returns:
            List of related services
        """
        # Find the reference service
        reference_service = None
        for indexed_item in self.search_index:
            if indexed_item["service"].get("id") == service_id:
                reference_service = indexed_item["service"]
                break

        if not reference_service:
            return []

        # Find services with similar category or keywords
        reference_category = reference_service.get("category", "")
        reference_keywords = set(
            reference_service.get("name_ar", "").lower().split()
        )

        related = []
        for indexed_item in self.search_index:
            if indexed_item["service"].get("id") == service_id:
                continue

            service = indexed_item["service"]
            service_category = service.get("category", "")

            # Same category match
            similarity = 0
            if service_category == reference_category:
                similarity += 2

            # Keyword overlap
            service_keywords = set(
                service.get("name_ar", "").lower().split()
            )
            overlap = len(reference_keywords & service_keywords)
            similarity += overlap

            if similarity > 0:
                related.append({
                    "service": service,
                    "platform": indexed_item["platform"],
                    "similarity_score": similarity,
                })

        # Sort by similarity and return
        related.sort(key=lambda x: x["similarity_score"], reverse=True)
        return related[:max_results]
