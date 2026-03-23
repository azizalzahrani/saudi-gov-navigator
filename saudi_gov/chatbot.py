"""
Chatbot Module - وحدة الدردشة الآلية

Interactive command-line chatbot for Saudi government service guidance.
دردشة آلية تفاعلية للتوجيه عبر خدمات الحكومة السعودية.
"""

from typing import Optional
from saudi_gov.agents.navigator_agent import NavigatorAgent
from saudi_gov.agents.service_finder import ServiceFinder
from saudi_gov.agents.requirements_agent import RequirementsAgent
from saudi_gov.search import SemanticSearch
from saudi_gov.config import Config


class SaudiGovChatbot:
    """
    Interactive chatbot for navigating Saudi government services.

    روبوت دردشة تفاعلي للتنقل في الخدمات الحكومية السعودية.
    """

    def __init__(self, language: str = "ar"):
        """
        Initialize the chatbot.

        Parameters:
            language: Interface language ("ar" for Arabic, "en" for English)
        """
        self.language = language
        self.navigator = NavigatorAgent(language=language)
        self.service_finder = ServiceFinder(language=language)
        self.requirements_agent = RequirementsAgent(language=language)
        self.search = SemanticSearch(language=language)
        self.config = Config()
        self.conversation_history = []

    def start(self) -> None:
        """Start the interactive chatbot session."""
        self._print_welcome_message()
        self._print_menu()

        while True:
            try:
                user_input = self._get_user_input()

                if not user_input:
                    continue

                response = self._process_input(user_input)

                if response is None:  # User chose to exit
                    print(
                        "\nشكراً لاستخدام دليل الخدمات الحكومية السعودية. وداعاً!"
                        if self.language == "ar"
                        else "\nThank you for using Saudi Gov Navigator. Goodbye!"
                    )
                    break

                print(f"\n{response}\n")
                print("-" * 60)

            except KeyboardInterrupt:
                print("\n\nوداعاً!" if self.language == "ar" else "\nGoodbye!")
                break
            except Exception as e:
                error_msg = f"خطأ: {str(e)}" if self.language == "ar" else f"Error: {str(e)}"
                print(error_msg)

    def _print_welcome_message(self) -> None:
        """Print welcome message."""
        if self.language == "ar":
            print("\n" + "=" * 60)
            print("🏛️  مرحباً بك في دليل الخدمات الحكومية السعودية")
            print("Saudi Gov Navigator")
            print("=" * 60)
            print("\nأنا هنا لمساعدتك في العثور على الخدمات الحكومية السعودية")
            print("والإجابة على أسئلتك حول المتطلبات والخطوات والرسوم.\n")
        else:
            print("\n" + "=" * 60)
            print("🏛️  Welcome to Saudi Government Services Navigator")
            print("دليل الخدمات الحكومية السعودية")
            print("=" * 60)
            print("\nI'm here to help you find Saudi government services")
            print("and answer questions about requirements, steps, and fees.\n")

    def _print_menu(self) -> None:
        """Print available commands."""
        if self.language == "ar":
            print("📋 الأوامر المتاحة:")
            print("  1. ابحث عن خدمة - اكتب استعلامك أو أسم الخدمة")
            print("  2. اكتب 'المنصات' - لعرض جميع المنصات الحكومية")
            print("  3. اكتب 'الفئات' - لعرض فئات الخدمات")
            print("  4. اكتب 'مساعدة' - لعرض معلومات المساعدة")
            print("  5. اكتب 'خروج' - للخروج من البرنامج\n")
        else:
            print("📋 Available Commands:")
            print("  1. Search - Type your query or service name")
            print("  2. Type 'platforms' - View all government platforms")
            print("  3. Type 'categories' - View service categories")
            print("  4. Type 'help' - Show help information")
            print("  5. Type 'exit' - Exit the program\n")

    def _get_user_input(self) -> str:
        """Get input from user."""
        prompt = "أنت: " if self.language == "ar" else "You: "
        return input(prompt).strip()

    def _process_input(self, user_input: str) -> Optional[str]:
        """
        Process user input and return response.

        Args:
            user_input: User's input string

        Returns:
            Response string or None if user exits
        """
        # Store in conversation history
        self.conversation_history.append({"user": user_input})

        # Check for commands
        user_lower = user_input.lower()

        if user_lower in ["خروج", "exit", "quit"]:
            return None

        elif user_lower in ["مساعدة", "help"]:
            return self._get_help()

        elif user_lower in ["المنصات", "platforms"]:
            return self._show_platforms()

        elif user_lower in ["الفئات", "categories"]:
            return self._show_categories()

        else:
            if self.service_finder.get_service_by_id(user_input):
                return self._show_service_details(user_input)

            # Treat as search query
            return self._handle_search_query(user_input)

    def _handle_search_query(self, query: str) -> str:
        """Handle service search query."""
        results = self.search.search(query, max_results=5)

        if not results:
            return (
                "عذراً، لم أتمكن من العثور على خدمات مطابقة. جرب مع كلمات مختلفة."
                if self.language == "ar"
                else "Sorry, I couldn't find matching services. Try with different keywords."
            )

        # Build response
        response_lines = []

        if self.language == "ar":
            response_lines.append("✅ وجدت الخدمات التالية:\n")
        else:
            response_lines.append("✅ Found the following services:\n")

        for idx, result in enumerate(results, 1):
            service = result["service"]
            name = service.get("name_ar" if self.language == "ar" else "name_en")
            desc = service.get("description_ar" if self.language == "ar" else "description_en")
            service_id = service.get("id")

            response_lines.append(f"{idx}. {name}")
            response_lines.append(f"   {desc}")
            response_lines.append(f"   [ID: {service_id}]\n")

        if self.language == "ar":
            response_lines.append("للحصول على التفاصيل، اكتب معرف الخدمة (ID)")
        else:
            response_lines.append("For more details, type the service ID")

        return "\n".join(response_lines)

    def _show_service_details(self, service_id: str) -> str:
        """Show the full guide for a selected service ID."""
        guide = self.requirements_agent.get_full_service_guide(service_id)
        if not guide:
            return (
                "الخدمة غير موجودة."
                if self.language == "ar"
                else "Service not found."
            )

        lines = [f"🏛️ {guide.get('name', service_id)}"]
        lines.append(guide.get("description", ""))
        lines.append("")

        fees = guide.get("fees", {})
        if self.language == "ar":
            lines.append(f"💰 الرسوم: {fees.get('note', 'غير محددة')}")
            lines.append(
                f"⏱️ وقت المعالجة: {guide.get('processing_time', 'غير محدد')}"
            )
            lines.append("📋 المتطلبات:")
        else:
            lines.append(f"💰 Fees: {fees.get('note', 'Not specified')}")
            lines.append(
                f"⏱️ Processing time: {guide.get('processing_time', 'Not specified')}"
            )
            lines.append("📋 Requirements:")

        for idx, requirement in enumerate(guide.get("requirements", []), 1):
            lines.append(f"{idx}. {requirement}")

        if guide.get("steps"):
            lines.append("")
            lines.append("📝 الخطوات:" if self.language == "ar" else "📝 Steps:")
            for idx, step in enumerate(guide["steps"], 1):
                lines.append(f"{idx}. {step}")

        if guide.get("tips"):
            lines.append("")
            lines.append("💡 نصائح:" if self.language == "ar" else "💡 Tips:")
            for tip in guide["tips"][:3]:
                lines.append(f"- {tip}")

        return "\n".join(lines)

    def _show_platforms(self) -> str:
        """Show all government platforms."""
        platforms = self.service_finder.get_all_platforms()

        response_lines = []

        if self.language == "ar":
            response_lines.append("🏢 المنصات الحكومية المتاحة:\n")
        else:
            response_lines.append("🏢 Available Government Platforms:\n")

        for idx, (platform_ar, platform_code) in enumerate(platforms.items(), 1):
            info = self.service_finder.get_platform_info(platform_ar)
            if info:
                response_lines.append(f"{idx}. {info['name_ar']} ({info['name_en']})")
                response_lines.append(f"   الخدمات: {info['services_count']}")
                response_lines.append(f"   {info.get('description_ar', '')}\n")

        return "\n".join(response_lines)

    def _show_categories(self) -> str:
        """Show service categories."""
        categories = self.service_finder.categorize_services()

        response_lines = []

        if self.language == "ar":
            response_lines.append("📂 فئات الخدمات:\n")
        else:
            response_lines.append("📂 Service Categories:\n")

        for idx, (category, services) in enumerate(categories.items(), 1):
            response_lines.append(f"{idx}. {category} ({len(services)} خدمة)" if self.language == "ar"
                                else f"{idx}. {category} ({len(services)} services)")

        return "\n".join(response_lines)

    def _get_help(self) -> str:
        """Get help information."""
        if self.language == "ar":
            return (
                "📚 معلومات المساعدة:\n\n"
                "هذا البرنامج يساعدك في البحث عن الخدمات الحكومية السعودية.\n\n"
                "يمكنك:\n"
                "• البحث عن خدمة - اكتب أسم الخدمة أو وصفها\n"
                "• عرض المنصات - اكتب 'المنصات'\n"
                "• عرض الفئات - اكتب 'الفئات'\n"
                "• الخروج - اكتب 'خروج'\n\n"
                "لكل خدمة ستجد معلومات عن المتطلبات والخطوات والرسوم."
            )
        else:
            return (
                "📚 Help Information:\n\n"
                "This program helps you find Saudi government services.\n\n"
                "You can:\n"
                "• Search for a service - type the service name or description\n"
                "• View platforms - type 'platforms'\n"
                "• View categories - type 'categories'\n"
                "• Exit - type 'exit'\n\n"
                "For each service you'll find information about requirements, steps, and fees."
            )


def main() -> None:
    """Main entry point for the chatbot."""
    # Detect language from environment or use default
    import os
    language = os.getenv("LANGUAGE", "ar")

    chatbot = SaudiGovChatbot(language=language)
    chatbot.start()


if __name__ == "__main__":
    main()
