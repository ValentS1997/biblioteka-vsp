#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

import yaml

from build_dynamic_ir_ru_book import (
    BOOK_ID,
    BOOK_TITLE_RU,
    BOOK_SUBTITLE_RU,
    ORIGINAL_TITLE,
    AUTHOR,
    YEAR,
    LICENSE,
    split_frontmatter,
    chapter_num,
    build_reference_docx,
)

HEADING_REPLACEMENTS = {

    "РАЗНЫЕ, НО СВЯЗАННЫЕ: POLICIES, PLANS И PLAYBOOKS": "РАЗНЫЕ, НО СВЯЗАННЫЕ: ПОЛИТИКИ, ПЛАНЫ И ПЛЕЙБУКИ",
    "ПОЛУЧЕНИЕ MANAGEMENT SUPPORT ДЛЯ РАЗРАБОТКИ POLICY": "ПОЛУЧЕНИЕ ПОДДЕРЖКИ РУКОВОДСТВА ДЛЯ РАЗРАБОТКИ ПОЛИТИКИ",
    "РАЗРАБОТКА ОРГАНИЗАЦИОННЫХ POLICIES": "РАЗРАБОТКА ОРГАНИЗАЦИОННЫХ ПОЛИТИК",
    "ПРИМЕРЫ INCIDENT RESPONSE POLICY И PLAN TEMPLATES": "ПРИМЕРЫ ШАБЛОНОВ ПОЛИТИКИ И ПЛАНА РЕАГИРОВАНИЯ НА ИНЦИДЕНТЫ",
    "РАЗВИТИЕ MANAGEMENT SUPPORT": "РАЗВИТИЕ ПОДДЕРЖКИ РУКОВОДСТВА",
    "BROAD VS. SPECIFIC RISK ASSESSMENT CRITERIA": "ОБЩИЕ И СПЕЦИФИЧЕСКИЕ КРИТЕРИИ ОЦЕНКИ РИСКА",
    "РАЗРАБОТКА INCIDENT COMMUNICATIONS PLAN": "РАЗРАБОТКА ПЛАНА КОММУНИКАЦИЙ ПРИ ИНЦИДЕНТЕ",
    "СОЗДАНИЕ COMMUNICATION CHANNELS": "СОЗДАНИЕ КАНАЛОВ КОММУНИКАЦИИ",
    "ДОКУМЕНТИРОВАНИЕ CONTACT INFORMATION": "ДОКУМЕНТИРОВАНИЕ КОНТАКТНОЙ ИНФОРМАЦИИ",
    "EXTERNAL REPORTING CHANNELS": "ВНЕШНИЕ КАНАЛЫ УВЕДОМЛЕНИЯ",
    "REPORTING PROCEDURES": "ПРОЦЕДУРЫ УВЕДОМЛЕНИЯ",
    "EMERGENCY COMMUNICATION PLAN": "ПЛАН ЭКСТРЕННЫХ КОММУНИКАЦИЙ",
    "СОЗДАНИЕ INCIDENT RESPONSE TEAM": "СОЗДАНИЕ КОМАНДЫ РЕАГИРОВАНИЯ НА ИНЦИДЕНТЫ",
    "VIRTUAL VS DEDICATED INCIDENT RESPONSE TEAMS": "ВИРТУАЛЬНЫЕ И ВЫДЕЛЕННЫЕ КОМАНДЫ РЕАГИРОВАНИЯ",
    "INCIDENT TRACKING PLATFORM": "ПЛАТФОРМА УЧЁТА ИНЦИДЕНТОВ",
    "УЧЁТ ТРЕБОВАНИЙ CYBER INSURANCE": "УЧЁТ ТРЕБОВАНИЙ КИБЕРСТРАХОВАНИЯ",
    "SECURITY AWARENESS TRAINING": "ОБУЧЕНИЕ ОСНОВАМ ИНФОРМАЦИОННОЙ БЕЗОПАСНОСТИ",
    "ПОДГОТОВКА INCIDENT RESPONSE TEAM": "ПОДГОТОВКА КОМАНДЫ РЕАГИРОВАНИЯ",
    "BACKUP И RECOVERY PROCEDURES": "ПРОЦЕДУРЫ РЕЗЕРВНОГО КОПИРОВАНИЯ И ВОССТАНОВЛЕНИЯ",
    "RELATIONSHIPS С ESSENTIAL PERSONNEL": "ВЗАИМОДЕЙСТВИЕ С КЛЮЧЕВЫМ ПЕРСОНАЛОМ",
    "DOCUMENT INCIDENT RESPONSE DECISION AUTHORITY": "ДОКУМЕНТИРОВАНИЕ ПОЛНОМОЧИЙ ПО ПРИНЯТИЮ РЕШЕНИЙ",
    "PLAYBOOKS ДЛЯ COMMON INCIDENTS": "ПЛЕЙБУКИ ДЛЯ ТИПОВЫХ ИНЦИДЕНТОВ",
    "ПОДГОТОВКА RESOURCES ДЛЯ RESPONSE ACTIONS": "ПОДГОТОВКА РЕСУРСОВ ДЛЯ ДЕЙСТВИЙ РЕАГИРОВАНИЯ",
    "ПОДГОТОВКА ACCESS К SYSTEMS": "ПОДГОТОВКА ДОСТУПА К СИСТЕМАМ",
    "TABLETOP EXERCISES И INCIDENT RESPONSE DRILLS": "НАСТОЛЬНЫЕ УЧЕНИЯ И ТРЕНИРОВКИ ПО РЕАГИРОВАНИЮ",
    "PROACTIVE PREVENTION AND DETECTION": "ПРОАКТИВНОЕ ПРЕДОТВРАЩЕНИЕ И ОБНАРУЖЕНИЕ",
    "CYBER THREAT INTELLIGENCE (CTI) CAPABILITIES": "ВОЗМОЖНОСТИ КИБЕРРАЗВЕДКИ (CTI)",
    "SOFTWARE MANAGEMENT PROCESSES И PROCEDURES": "ПРОЦЕССЫ И ПРОЦЕДУРЫ УПРАВЛЕНИЯ ПО",
    "PATCH, CONFIGURATION И INVENTORY": "ПАТЧИ, КОНФИГУРАЦИЯ И ИНВЕНТАРИЗАЦИЯ",
    "SYSTEM HARDENING": "УКРЕПЛЕНИЕ СИСТЕМ",
    "ENDPOINT-BASED SECURITY MONITORING И THREAT DETECTION": "МОНИТОРИНГ КОНЕЧНЫХ ТОЧЕК И ОБНАРУЖЕНИЕ УГРОЗ",
    "NETWORK SECURITY MONITORING И THREAT DETECTION": "СЕТЕВОЙ МОНИТОРИНГ БЕЗОПАСНОСТИ И ОБНАРУЖЕНИЕ УГРОЗ",
    "INVEST IN DETECTION ENGINEERING": "ИНВЕСТИРУЙТЕ В DETECTION ENGINEERING",
    "THREAT HUNTING PROGRAM": "ПРОГРАММА ПОИСКА УГРОЗ",
    "MONITOR THE ATTACK SURFACE": "МОНИТОРИНГ ПОВЕРХНОСТИ АТАКИ",
    "COLLECT AND RETAIN LOGGING INFORMATION": "СБОР И ХРАНЕНИЕ ЖУРНАЛОВ",
    "PREPARATION CHALLENGES": "СЛОЖНОСТИ ПОДГОТОВКИ",
    "RESOURCE CONSTRAINTS": "ОГРАНИЧЕНИЯ РЕСУРСОВ",
    "ORGANIZATIONAL CHANGE И TURNOVER": "ОРГАНИЗАЦИОННЫЕ ИЗМЕНЕНИЯ И ТЕКУЧЕСТЬ КАДРОВ",
    "ДЕМОНСТРАЦИЯ ЦЕННОСТИ БЕЗ INCIDENTS": "ДЕМОНСТРАЦИЯ ЦЕННОСТИ БЕЗ ИНЦИДЕНТОВ",
    "ПРИМЕРЫ PREPARE ACTIVITY": "ПРИМЕРЫ ЭТАПА ПОДГОТОВКИ",

    "SIGNATURE-BASED DETECTION": "СИГНАТУРНОЕ ОБНАРУЖЕНИЕ",
    "BEHAVIORAL DETECTION": "ПОВЕДЕНЧЕСКОЕ ОБНАРУЖЕНИЕ",
    "SCOPING BASELINES TO BUSINESS UNITS": "ФОРМИРОВАНИЕ БАЗОВЫХ ЛИНИЙ ПО БИЗНЕС-ПОДРАЗДЕЛЕНИЯМ",
    "MACHINE LEARNING DETECTION": "ОБНАРУЖЕНИЕ С ПОМОЩЬЮ МАШИННОГО ОБУЧЕНИЯ",
    "HYBRID DETECTION APPROACHES": "ГИБРИДНЫЕ ПОДХОДЫ К ОБНАРУЖЕНИЮ",
    "ACTIVE VS. PASSIVE DETECTION": "АКТИВНОЕ И ПАССИВНОЕ ОБНАРУЖЕНИЕ",
    "THE TYRANNY OF INFINITE CHOICE": "ТИРАНИЯ БЕСКОНЕЧНОГО ВЫБОРА",
    "DETECTION DATA SOURCES": "ИСТОЧНИКИ ДАННЫХ ДЛЯ ОБНАРУЖЕНИЯ",
    "TECHNICAL DETECTION SOURCES": "ТЕХНИЧЕСКИЕ ИСТОЧНИКИ ОБНАРУЖЕНИЯ",
    "OPENOBSERVE: OPEN SOURCE LOG ANALYSIS": "OPENOBSERVE: OPEN-SOURCE АНАЛИЗ ЖУРНАЛОВ",
    "RITA: OPEN SOURCE NETWORK THREAT ANALYSIS": "RITA: OPEN-SOURCE АНАЛИЗ СЕТЕВЫХ УГРОЗ",
    "HUMAN DETECTION SOURCES": "ЧЕЛОВЕЧЕСКИЕ ИСТОЧНИКИ ОБНАРУЖЕНИЯ",
    "CLOUD-NATIVE DETECTION SOURCES": "ВСТРОЕННЫЕ ОБЛАЧНЫЕ ИСТОЧНИКИ ОБНАРУЖЕНИЯ",
    "CONTAINER AND KUBERNETES DETECTION": "ОБНАРУЖЕНИЕ В КОНТЕЙНЕРАХ И KUBERNETES",
    "SERVERLESS AND MICROSERVICES DETECTION": "ОБНАРУЖЕНИЕ В SERVERLESS И МИКРОСЕРВИСАХ",
    "HYBRID CLOUD": "ГИБРИДНОЕ ОБЛАКО",
    "CHALLENGES IN DETECTION": "СЛОЖНОСТИ ОБНАРУЖЕНИЯ",
    "DATA VOLUME AND VELOCITY": "ОБЪЁМ И СКОРОСТЬ ПОСТУПЛЕНИЯ ДАННЫХ",
    "DETECTION-DRIVEN COLLECTION: AZURE STORAGE LOGGING": "СБОР ДАННЫХ, УПРАВЛЯЕМЫЙ ЗАДАЧАМИ ОБНАРУЖЕНИЯ: AZURE STORAGE",
    "ENCRYPTED TRAFFIC": "ЗАШИФРОВАННЫЙ ТРАФИК",
    "ENCRYPTED TRAFFIC DETECTION TECHNIQUES": "МЕТОДЫ ОБНАРУЖЕНИЯ В ЗАШИФРОВАННОМ ТРАФИКЕ",
    "ADVERSARY EVASION": "УКЛОНЕНИЕ АТАКУЮЩЕГО ОТ ОБНАРУЖЕНИЯ",
    "THE PRE-ATTACK LAB": "ЛАБОРАТОРИЯ ДО АТАКИ",
    "SKILLS GAP": "ДЕФИЦИТ КОМПЕТЕНЦИЙ",
    "DETECT ACTIVITY EXAMPLES": "ПРИМЕРЫ ЭТАПА ОБНАРУЖЕНИЯ",
    "THE EXTERNAL BREACH HUNTER": "ВНЕШНИЙ ИССЛЕДОВАТЕЛЬ КОМПРОМЕТАЦИИ",
    "THE SIEM WIZARD": "ЭКСПЕРТ ПО SIEM",
    "DETECT: STEP-BY-STEP": "ОБНАРУЖЕНИЕ: ПОШАГОВО",

    "VERIFICATION AS A GATING FUNCTION": "ПРОВЕРКА КАК КОНТРОЛЬНАЯ ТОЧКА",
    "VERIFICATION RESPONSE ACTIONS": "ДЕЙСТВИЯ ПРИ ПРОВЕРКЕ",
    "THE NEED FOR PRISTINE DOCUMENTATION": "НЕОБХОДИМОСТЬ БЕЗУПРЕЧНОЙ ДОКУМЕНТАЦИИ",
    "VERIFICATION AND CYBER THREAT INTELLIGENCE": "ПРОВЕРКА И КИБЕРРАЗВЕДКА",
    "EOI VALIDATION AND ENRICHMENT": "ПРОВЕРКА И ОБОГАЩЕНИЕ EOI",
    "INFORMING INITIAL RISK CLASSIFICATION": "УТОЧНЕНИЕ НАЧАЛЬНОЙ КЛАССИФИКАЦИИ РИСКА",
    "SAME DOMAIN, TWO RISK ASSESSMENTS": "ОДИН ДОМЕН, ДВЕ ОЦЕНКИ РИСКА",
    "PIVOTING TO RELATED INDICATORS": "ПЕРЕХОД К СВЯЗАННЫМ ИНДИКАТОРАМ",
    "VERIFICATION ACTIVITY EXAMPLES": "ПРИМЕРЫ ЭТАПА ПРОВЕРКИ",
    "THE UNRESPONSIVE WORDPRESS SITE": "НЕОТВЕЧАЮЩИЙ САЙТ WORDPRESS",
    "THE UNPAID TOLL": "НЕОПЛАЧЕННЫЙ ДОРОЖНЫЙ СБОР",
    "THE SIMPLE, SECURE STORAGE BUCKET": "ПРОСТОЙ И БЕЗОПАСНЫЙ STORAGE BUCKET",
    "A TEMPERAMENTAL SERVER": "КАПРИЗНЫЙ СЕРВЕР",
    "TRIAGE ACTIVITY": "ЭТАП ТРИАЖА",
    "PRESENTING THE INCIDENT": "ПРЕДСТАВЛЕНИЕ ИНЦИДЕНТА",
    "TRIAGE EXAMPLE: THE THIRD-PARTY VENDOR BREACH": "ПРИМЕР ТРИАЖА: КОМПРОМЕТАЦИЯ СТОРОННЕГО ПОСТАВЩИКА",
    "VERIFY AND TRIAGE: STEP-BY-STEP": "ПРОВЕРКА И ТРИАЖ: ПОШАГОВО",

    "ON THE ITERATIVE NATURE OF INCIDENT RESPONSE": "ОБ ИТЕРАТИВНОЙ ПРИРОДЕ РЕАГИРОВАНИЯ НА ИНЦИДЕНТЫ",
    "THE FOUR RESPONSE ACTIONS LOOP ACTIVITIES": "ЧЕТЫРЕ ЭТАПА ЦИКЛА ДЕЙСТВИЙ РЕАГИРОВАНИЯ",
    "SCOPE: UNDERSTANDING BREADTH": "ОПРЕДЕЛЕНИЕ МАСШТАБА: ПОНИМАНИЕ ОХВАТА",
    "CONTAIN: STOPPING THE BLEEDING": "СДЕРЖИВАНИЕ: ОСТАНОВИТЬ РАЗВИТИЕ ИНЦИДЕНТА",
    "ERADICATE: REMOVING THE THREAT": "ИСКОРЕНЕНИЕ: УДАЛЕНИЕ УГРОЗЫ",
    "RECOVER: RESTORING OPERATIONS": "ВОССТАНОВЛЕНИЕ: ВОЗВРАТ К РАБОТЕ",
    "NEW INDICATORS OF COMPROMISE": "НОВЫЕ ИНДИКАТОРЫ КОМПРОМЕТАЦИИ",
    "SCOPE EXPANSION": "РАСШИРЕНИЕ МАСШТАБА",
    "INCOMPLETE ERADICATION": "НЕПОЛНОЕ ИСКОРЕНЕНИЕ",
    "EVIDENCE ANALYSIS REVELATIONS": "НОВЫЕ ДАННЫЕ ИЗ АНАЛИЗА ДОКАЗАТЕЛЬСТВ",
    "CHANGING BUSINESS PRIORITIES AND OBLIGATIONS": "ИЗМЕНЕНИЕ БИЗНЕС-ПРИОРИТЕТОВ И ОБЯЗАТЕЛЬСТВ",
    "DOCUMENTATION AND COMMUNICATION": "ДОКУМЕНТИРОВАНИЕ И КОММУНИКАЦИЯ",
    "DECISION DOCUMENTATION": "ДОКУМЕНТИРОВАНИЕ РЕШЕНИЙ",
    "IMPACT ASSESSMENT": "ОЦЕНКА ВЛИЯНИЯ",
    "RESOURCE MANAGEMENT": "УПРАВЛЕНИЕ РЕСУРСАМИ",
    "DOCUMENTATION BURDEN": "НАГРУЗКА ПО ДОКУМЕНТИРОВАНИЮ",
    "STAKEHOLDER PATIENCE": "ТЕРПЕНИЕ ЗАИНТЕРЕСОВАННЫХ СТОРОН",
    "RESPONSE ACTIONS LOOP: STEP-BY-STEP": "ЦИКЛ ДЕЙСТВИЙ РЕАГИРОВАНИЯ: ПОШАГОВО",

    "THE PURPOSE OF SCOPING": "ЦЕЛЬ ОПРЕДЕЛЕНИЯ МАСШТАБА",
    "INDICATORS OF COMPROMISE IN SCOPING": "ИНДИКАТОРЫ КОМПРОМЕТАЦИИ ПРИ ОПРЕДЕЛЕНИИ МАСШТАБА",
    "TECHNICAL IOCS": "ТЕХНИЧЕСКИЕ IOC",
    "BEHAVIORAL IOCS": "ПОВЕДЕНЧЕСКИЕ IOC",
    "SCOPING METHODOLOGIES": "МЕТОДЫ ОПРЕДЕЛЕНИЯ МАСШТАБА",
    "ENTERPRISE-WIDE HUNTING": "ПОИСК УГРОЗ В МАСШТАБЕ ОРГАНИЗАЦИИ",
    "PROGRESSIVE SCOPING": "ПОСТЕПЕННОЕ РАСШИРЕНИЕ МАСШТАБА",
    "TIMELINE RECONSTRUCTION": "ВОССТАНОВЛЕНИЕ ХРОНОЛОГИИ",
    "SCOPING CHALLENGES": "СЛОЖНОСТИ ОПРЕДЕЛЕНИЯ МАСШТАБА",
    "VISIBILITY GAPS": "ПРОБЕЛЫ В НАБЛЮДАЕМОСТИ",
    "CLOUD AND HYBRID ENVIRONMENTS": "ОБЛАЧНЫЕ И ГИБРИДНЫЕ СРЕДЫ",
    "ANTI-FORENSIC TECHNIQUES": "АНТИФОРЕНЗИК-МЕТОДЫ",
    "LOG DELETION AND MODIFICATION": "УДАЛЕНИЕ И ИЗМЕНЕНИЕ ЖУРНАЛОВ",
    "TIMESTOMPING": "ИЗМЕНЕНИЕ ВРЕМЕННЫХ МЕТОК",
    "ENCRYPTION AND OBFUSCATION": "ШИФРОВАНИЕ И ОБФУСКАЦИЯ",
    "LIVING OFF THE LAND": "LIVING OFF THE LAND",
    "SCALE AND COMPLEXITY": "МАСШТАБ И СЛОЖНОСТЬ",
    "DYNAMIC / CLOUD ENVIRONMENTS": "ДИНАМИЧЕСКИЕ И ОБЛАЧНЫЕ СРЕДЫ",
    "INTEGRATION WITH RESPONSE ACTIVITIES": "ИНТЕГРАЦИЯ С ДРУГИМИ ЭТАПАМИ РЕАГИРОВАНИЯ",
    "SCOPE ACTIVITY EXAMPLES": "ПРИМЕРЫ ОПРЕДЕЛЕНИЯ МАСШТАБА",
    "THE LINKEDIN ATTACHMENT": "ВЛОЖЕНИЕ ИЗ LINKEDIN",
    "THE CLOUD STORAGE EXFILTRATION": "ЭКСФИЛЬТРАЦИЯ В ОБЛАЧНОЕ ХРАНИЛИЩЕ",
    "SCOPE: STEP-BY-STEP": "ОПРЕДЕЛЕНИЕ МАСШТАБА: ПОШАГОВО",

    "CONTAINMENT OBJECTIVES": "ЦЕЛИ СДЕРЖИВАНИЯ",
    "STOPPING ATTACKER ACTIVITY": "ПРЕКРАЩЕНИЕ АКТИВНОСТИ АТАКУЮЩЕГО",
    "EVIDENCE COLLECTION AND PRESERVATION": "СБОР И СОХРАНЕНИЕ ДОКАЗАТЕЛЬСТВ",
    "CONTAINMENT STRATEGIES": "СТРАТЕГИИ СДЕРЖИВАНИЯ",
    "PASSIVE CONTAINMENT": "ПАССИВНОЕ СДЕРЖИВАНИЕ",
    "ACTIVE CONTAINMENT": "АКТИВНОЕ СДЕРЖИВАНИЕ",
    "ADAPTIVE CONTAINMENT": "АДАПТИВНОЕ СДЕРЖИВАНИЕ",
    "TIMING AND COORDINATION": "ВЫБОР МОМЕНТА И КООРДИНАЦИЯ",
    "COORDINATED CONTAINMENT": "СКООРДИНИРОВАННОЕ СДЕРЖИВАНИЕ",
    "TECHNICAL IMPLEMENTATION": "ТЕХНИЧЕСКАЯ РЕАЛИЗАЦИЯ",
    "NETWORK-LEVEL CONTAINMENT": "СДЕРЖИВАНИЕ НА СЕТЕВОМ УРОВНЕ",
    "HOST-LEVEL CONTAINMENT": "СДЕРЖИВАНИЕ НА УРОВНЕ ХОСТА",
    "APPLICATION-LEVEL CONTAINMENT": "СДЕРЖИВАНИЕ НА УРОВНЕ ПРИЛОЖЕНИЯ",
    "IDENTITY AND ACCESS MANAGEMENT CONTAINMENT": "СДЕРЖИВАНИЕ ЧЕРЕЗ УПРАВЛЕНИЕ ИДЕНТИЧНОСТЯМИ И ДОСТУПОМ",
    "ACTIVE SESSION TERMINATION": "ЗАВЕРШЕНИЕ АКТИВНЫХ СЕССИЙ",
    "RESIDUAL-ACCESS WINDOW": "ОКНО ОСТАТОЧНОГО ДОСТУПА",
    "REFRESH TOKEN AND PERSISTENT CREDENTIAL REVOCATION": "ОТЗЫВ REFRESH-TOKEN И ПОСТОЯННЫХ УЧЁТНЫХ ДАННЫХ",
    "EVIDENCE COLLECTION DURING CONTAINMENT": "СБОР ДОКАЗАТЕЛЬСТВ ВО ВРЕМЯ СДЕРЖИВАНИЯ",
    "CLOUD CONTAINMENT": "СДЕРЖИВАНИЕ В ОБЛАКЕ",
    "CONTAINMENT CHALLENGES": "СЛОЖНОСТИ СДЕРЖИВАНИЯ",
    "REMOTE WORKER ENVIRONMENTS": "СРЕДЫ УДАЛЁННЫХ СОТРУДНИКОВ",
    "BEYOND TRADITIONAL HOST COMPROMISE": "ЗА ПРЕДЕЛАМИ КЛАССИЧЕСКОЙ КОМПРОМЕТАЦИИ ХОСТА",
    "CONTAINMENT VALIDATION": "ПРОВЕРКА СДЕРЖИВАНИЯ",
    "CONTAIN ACTIVITY EXAMPLES": "ПРИМЕРЫ СДЕРЖИВАНИЯ",
    "CONTAIN: STEP-BY-STEP": "СДЕРЖИВАНИЕ: ПОШАГОВО",

    "ERADICATE OBJECTIVES": "ЦЕЛИ ИСКОРЕНЕНИЯ",
    "PREVENTING INCIDENT RECURRENCE THROUGH INVESTIGATION": "ПРЕДОТВРАЩЕНИЕ ПОВТОРЕНИЯ ИНЦИДЕНТА ЧЕРЕЗ РАССЛЕДОВАНИЕ",
    "INVESTIGATION DURING ERADICATION": "РАССЛЕДОВАНИЕ ВО ВРЕМЯ ИСКОРЕНЕНИЯ",
    "SHORT-FORM INVESTIGATION": "КРАТКОЕ РАССЛЕДОВАНИЕ",
    "LONG-FORM INVESTIGATION FOR COMPREHENSIVE UNDERSTANDING": "УГЛУБЛЁННОЕ РАССЛЕДОВАНИЕ ДЛЯ ПОЛНОГО ПОНИМАНИЯ",
    "PURSUING ROOT CAUSE ANALYSIS": "ПОИСК КОРНЕВОЙ ПРИЧИНЫ",
    "FOUR P'S FRAMEWORK": "ФРЕЙМВОРК ЧЕТЫРЁХ P",
    "FISHBONE DIAGRAM MAPPING": "ПОСТРОЕНИЕ ДИАГРАММЫ ИСИКАВЫ",
    "INVESTIGATION TECHNIQUES FOR ERADICATION": "МЕТОДЫ РАССЛЕДОВАНИЯ ДЛЯ ИСКОРЕНЕНИЯ",
    "LOG INVESTIGATION": "АНАЛИЗ ЖУРНАЛОВ",
    "SIEM FOR LOG INVESTIGATION": "SIEM ДЛЯ АНАЛИЗА ЖУРНАЛОВ",
    "LIVE INVESTIGATION": "ИССЛЕДОВАНИЕ ЖИВОЙ СИСТЕМЫ",
    "ENDPOINT TELEMETRY INVESTIGATION TOOLS": "СРЕДСТВА АНАЛИЗА ТЕЛЕМЕТРИИ КОНЕЧНЫХ ТОЧЕК",
    "MEMORY INVESTIGATION": "АНАЛИЗ ПАМЯТИ",
    "NETWORK INVESTIGATION": "СЕТЕВОЕ РАССЛЕДОВАНИЕ",
    "MALWARE INVESTIGATION": "АНАЛИЗ ВРЕДОНОСНОГО ПО",
    "BUSINESS EMAIL COMPROMISE INVESTIGATION": "РАССЛЕДОВАНИЕ КОМПРОМЕТАЦИИ ДЕЛОВОЙ ПОЧТЫ",
    "IDENTITY AND ACCESS INVESTIGATION": "РАССЛЕДОВАНИЕ ИДЕНТИЧНОСТЕЙ И ДОСТУПА",
    "INSIDER THREAT INVESTIGATION": "РАССЛЕДОВАНИЕ ВНУТРЕННИХ УГРОЗ",
    "SUPPLIER AND SUPPLY CHAIN INVESTIGATION": "РАССЛЕДОВАНИЕ ПОСТАВЩИКОВ И ЦЕПОЧКИ ПОСТАВОК",
    "CLOUD INVESTIGATION": "ОБЛАЧНОЕ РАССЛЕДОВАНИЕ",
    "ERADICATE ATTACKER ACCESS": "УСТРАНЕНИЕ ДОСТУПА АТАКУЮЩЕГО",
    "REMOVING PERSISTENCE MECHANISMS": "УДАЛЕНИЕ МЕХАНИЗМОВ ЗАКРЕПЛЕНИЯ",
    "ACCOUNT AND IDENTITY REMEDIATION": "ИСПРАВЛЕНИЕ УЧЁТНЫХ ЗАПИСЕЙ И ИДЕНТИЧНОСТЕЙ",
    "KRBTGT ACCOUNT RESET": "СБРОС УЧЁТНОЙ ЗАПИСИ KRBTGT",
    "HYBRID AND ENTRA ID REMEDIATION": "ИСПРАВЛЕНИЕ HYBRID-СРЕДЫ И ENTRA ID",
    "TARGETED REMOVAL VS. SYSTEM REBUILD": "ТОЧЕЧНОЕ УДАЛЕНИЕ ИЛИ ПЕРЕСБОРКА СИСТЕМЫ",
    "VULNERABILITY REMEDIATION": "УСТРАНЕНИЕ УЯЗВИМОСТЕЙ",
    "ERADICATION CHALLENGES": "СЛОЖНОСТИ ИСКОРЕНЕНИЯ",
    "FILELESS MALWARE": "БЕСФАЙЛОВОЕ ВРЕДОНОСНОЕ ПО",
    "ERADICATE ACTIVITY EXAMPLES": "ПРИМЕРЫ ИСКОРЕНЕНИЯ",
    "ERADICATE: STEP-BY-STEP": "ИСКОРЕНЕНИЕ: ПОШАГОВО",

    "RECOVERY OBJECTIVES": "ЦЕЛИ ВОССТАНОВЛЕНИЯ",
    "PRE-RESTORATION VERIFICATION": "ПРОВЕРКА ПЕРЕД ВОССТАНОВЛЕНИЕМ",
    "SYSTEM VALIDATION TESTING": "ПРОВЕРОЧНОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ",
    "SYSTEM OWNER ACCEPTANCE": "ПРИЁМКА ВЛАДЕЛЬЦЕМ СИСТЕМЫ",
    "ENHANCED MONITORING CONFIGURATION": "НАСТРОЙКА УСИЛЕННОГО МОНИТОРИНГА",
    "CONFIGURING PLATFORM-SPECIFIC LOGGING AND AUDITING": "НАСТРОЙКА ЖУРНАЛИРОВАНИЯ И АУДИТА ДЛЯ КОНКРЕТНОЙ ПЛАТФОРМЫ",
    "CUSTOM DETECTION AND MONITORING DURATION": "СПЕЦИАЛЬНЫЕ ПРАВИЛА ОБНАРУЖЕНИЯ И СРОК УСИЛЕННОГО МОНИТОРИНГА",
    "COORDINATED PRODUCTION RESTORATION": "СКООРДИНИРОВАННОЕ ВОЗВРАЩЕНИЕ В ПРОДАКШЕН",
    "RECOVERY RACI: WHO ACTUALLY DOES THIS WORK?": "RACI ДЛЯ ВОССТАНОВЛЕНИЯ: КТО ВЫПОЛНЯЕТ РАБОТЫ?",
    "RESTORATION TIMING": "ВЫБОР МОМЕНТА ВОССТАНОВЛЕНИЯ",
    "PHASED RESTORATION": "ПОЭТАПНОЕ ВОССТАНОВЛЕНИЕ",
    "CONTAINMENT ACTION REMOVAL": "СНЯТИЕ МЕР СДЕРЖИВАНИЯ",
    "METRICS CAPTURE": "СБОР МЕТРИК",
    "RECOVERY STRATEGIES": "СТРАТЕГИИ ВОССТАНОВЛЕНИЯ",
    "PHASED RECOVERY": "ПОЭТАПНОЕ ВОССТАНОВЛЕНИЕ",
    "COORDINATED RECOVERY": "СКООРДИНИРОВАННОЕ ВОССТАНОВЛЕНИЕ",
    "SCHEDULING CONSIDERATIONS": "АСПЕКТЫ ПЛАНИРОВАНИЯ",
    "CLOUD RECOVERY CONSIDERATIONS": "ОСОБЕННОСТИ ВОССТАНОВЛЕНИЯ В ОБЛАКЕ",
    "SNAPSHOT RESTORATION": "ВОССТАНОВЛЕНИЕ ИЗ СНАПШОТА",
    "IAM RECOVERY VALIDATION": "ПРОВЕРКА IAM ПОСЛЕ ВОССТАНОВЛЕНИЯ",
    "INFRASTRUCTURE AS CODE": "ИНФРАСТРУКТУРА КАК КОД",
    "RECOVERY CHALLENGES": "СЛОЖНОСТИ ВОССТАНОВЛЕНИЯ",
    "DATA LOSS FROM CLEAN-BACKUP RECOVERY": "ПОТЕРЯ ДАННЫХ ПРИ ВОССТАНОВЛЕНИИ ИЗ ЧИСТОЙ РЕЗЕРВНОЙ КОПИИ",
    "BUSINESS PRESSURE FOR RAPID RESTORATION": "ДАВЛЕНИЕ БИЗНЕСА В ПОЛЬЗУ БЫСТРОГО ВОССТАНОВЛЕНИЯ",
    "ERADICATION VERIFICATION UNCERTAINTY": "НЕОПРЕДЕЛЁННОСТЬ ПРИ ПРОВЕРКЕ ИСКОРЕНЕНИЯ",
    "COORDINATION COMPLEXITY": "СЛОЖНОСТЬ КООРДИНАЦИИ",
    "USER COMMUNICATION AND EXPECTATIONS": "КОММУНИКАЦИЯ С ПОЛЬЗОВАТЕЛЯМИ И УПРАВЛЕНИЕ ОЖИДАНИЯМИ",
    "POST-RECOVERY PROBLEM ATTRIBUTION": "АТРИБУЦИЯ ПРОБЛЕМ ПОСЛЕ ВОССТАНОВЛЕНИЯ",
    "RECOVER: STEP-BY-STEP": "ВОССТАНОВЛЕНИЕ: ПОШАГОВО",

    "DEBRIEF OBJECTIVES": "ЦЕЛИ РАЗБОРА ИНЦИДЕНТА",
    "INCIDENT CLOSURE": "ЗАКРЫТИЕ ИНЦИДЕНТА",
    "ORGANIZATIONAL LEARNING": "ОРГАНИЗАЦИОННОЕ ОБУЧЕНИЕ",
    "DEBRIEF STRATEGIES": "СТРАТЕГИИ РАЗБОРА ИНЦИДЕНТА",
    "TRANSITIONING TO DEBRIEF": "ПЕРЕХОД К РАЗБОРУ",
    "MANAGING TEMPORARY ASSETS": "УПРАВЛЕНИЕ ВРЕМЕННЫМИ РЕСУРСАМИ",
    "FORENSIC EVIDENCE RETENTION": "ХРАНЕНИЕ ФОРЕНЗИК-ДОКАЗАТЕЛЬСТВ",
    "CONSOLIDATING INCIDENT DOCUMENTATION": "КОНСОЛИДАЦИЯ ДОКУМЕНТАЦИИ ПО ИНЦИДЕНТУ",
    "DOCUMENTATION AND VALUE PROPOSITION": "ДОКУМЕНТАЦИЯ И ЕЁ ЦЕННОСТЬ",
    "LIGHTWEIGHT DOCUMENTATION": "ОБЛЕГЧЁННАЯ ДОКУМЕНТАЦИЯ",
    "FORMAL DOCUMENTATION": "ФОРМАЛЬНАЯ ДОКУМЕНТАЦИЯ",
    "CAPTURING INCIDENT METRICS": "СБОР МЕТРИК ИНЦИДЕНТА",
    "CONDUCTING THE AFTER-ACTION REVIEW": "ПРОВЕДЕНИЕ ПОСЛЕИНЦИДЕНТНОГО РАЗБОРА",
    "DRIVING ORGANIZATIONAL IMPROVEMENT": "ОРГАНИЗАЦИОННЫЕ УЛУЧШЕНИЯ",
    "DEVELOPING THE INCIDENT REPORT": "ПОДГОТОВКА ОТЧЁТА ОБ ИНЦИДЕНТЕ",
    "TWO-REPORT APPROACH": "ПОДХОД С ДВУМЯ ОТЧЁТАМИ",
    "INCIDENT SUMMARY REPORT": "КРАТКИЙ ОТЧЁТ ОБ ИНЦИДЕНТЕ",
    "EXECUTIVE REPORTING LEVERS": "РЫЧАГИ УПРАВЛЕНЧЕСКОЙ ОТЧЁТНОСТИ",
    "TECHNICAL INCIDENT RESPONSE REPORT": "ТЕХНИЧЕСКИЙ ОТЧЁТ О РЕАГИРОВАНИИ",
    "PRESENTING FINDINGS AND RECOMMENDATIONS": "ПРЕДСТАВЛЕНИЕ ВЫВОДОВ И РЕКОМЕНДАЦИЙ",
    "FOLLOW-UP AND ACCOUNTABILITY": "КОНТРОЛЬ И ОТВЕТСТВЕННОСТЬ",
    "DEBRIEF CHALLENGES": "СЛОЖНОСТИ РАЗБОРА",
    "DEBRIEF ACTIVITY EXAMPLES": "ПРИМЕРЫ РАЗБОРА ИНЦИДЕНТА",
    "SUSTAINING MOMENTUM": "ПОДДЕРЖАНИЕ ТЕМПА УЛУЧШЕНИЙ",
    "DEBRIEF: STEP-BY-STEP": "РАЗБОР ИНЦИДЕНТА: ПОШАГОВО",

    "OPPORTUNITIES AND CAUTIONS": "ВОЗМОЖНОСТИ И ОГРАНИЧЕНИЯ",
    "HALLUCINATION RISK": "РИСК ГАЛЛЮЦИНАЦИЙ",
    "NON-DETERMINISM": "НЕДЕТЕРМИНИРОВАННОСТЬ",
    "DATA HANDLING": "ОБРАБОТКА ДАННЫХ",
    "TRAINING CUTOFF / STALENESS": "ОГРАНИЧЕНИЯ ПО ДАТЕ ОБУЧЕНИЯ И УСТАРЕВАНИЕ",
    "DATA HANDLING CONSIDERATIONS": "АСПЕКТЫ ОБРАБОТКИ ДАННЫХ",
    "FRONTIER MODELS": "ПЕРЕДОВЫЕ МОДЕЛИ",
    "OPEN-WEIGHT MODELS": "МОДЕЛИ С ОТКРЫТЫМИ ВЕСАМИ",
    "DATA SANITIZATION": "САНИТИЗАЦИЯ ДАННЫХ",
    "STRUCTURED PROMPTS FOR COMPLEX TASKS": "СТРУКТУРИРОВАННЫЕ ЗАПРОСЫ ДЛЯ СЛОЖНЫХ ЗАДАЧ",
    "CODE ANALYSIS AND DEOBFUSCATION": "АНАЛИЗ КОДА И ДЕОБФУСКАЦИЯ",
    "LOG ANALYSIS AND ANOMALY DETECTION": "АНАЛИЗ ЖУРНАЛОВ И ОБНАРУЖЕНИЕ АНОМАЛИЙ",
    "LIMITATIONS OF AI LOG ANALYSIS": "ОГРАНИЧЕНИЯ ИИ-АНАЛИЗА ЖУРНАЛОВ",
    "TRANSLATING TECHNICAL FINDINGS FOR STAKEHOLDERS": "ПЕРЕВОД ТЕХНИЧЕСКИХ ВЫВОДОВ НА ЯЗЫК ЗАИНТЕРЕСОВАННЫХ СТОРОН",
    "GENERATING INCIDENT RESPONSE PLAYBOOKS": "ГЕНЕРАЦИЯ ПЛЕЙБУКОВ РЕАГИРОВАНИЯ",
    "DRAFTING INCIDENT REPORTS": "ПОДГОТОВКА ЧЕРНОВИКОВ ОТЧЁТОВ ОБ ИНЦИДЕНТАХ",
    "SPECIALIZED KNOWLEDGE INTEGRATION WITH MCP": "ИНТЕГРАЦИЯ СПЕЦИАЛИЗИРОВАННЫХ ЗНАНИЙ ЧЕРЕЗ MCP",
    "CREATING TABLETOP EXERCISE SCENARIOS": "СОЗДАНИЕ СЦЕНАРИЕВ НАСТОЛЬНЫХ УЧЕНИЙ",
    "SECURITY CONSIDERATIONS": "АСПЕКТЫ БЕЗОПАСНОСТИ",
    "MCP SUPPLY CHAIN AND REGISTRY RISKS": "РИСКИ ЦЕПОЧКИ ПОСТАВОК И РЕЕСТРОВ MCP",
    "FORENSIC ANALYSIS ACCELERATION WITH PROTOCOL SIFT": "УСКОРЕНИЕ ФОРЕНЗИК-АНАЛИЗА С PROTOCOL SIFT",
    "FROM TOOL USE TO TOOL ORCHESTRATION": "ОТ ИСПОЛЬЗОВАНИЯ ИНСТРУМЕНТОВ К ИХ ОРКЕСТРАЦИИ",
    "REACT AGENTS": "АГЕНТЫ REACT",
    "HUMAN IN THE LOOP (HITL)": "ЧЕЛОВЕК В КОНТУРЕ (HITL)",

    "THE UNTRACEABLE CREDENTIAL PROBLEM": "ПРОБЛЕМА НЕОТСЛЕЖИВАЕМЫХ УЧЁТНЫХ ДАННЫХ",
    "LEGITIMATE RMM AS ATTACKER INFRASTRUCTURE": "ЛЕГИТИМНЫЕ RMM КАК ИНФРАСТРУКТУРА АТАКУЮЩЕГО",
    "INITIAL ACCESS BROKERS": "БРОКЕРЫ ПЕРВОНАЧАЛЬНОГО ДОСТУПА",
    "INFRASTRUCTURE TARGETS": "ЦЕЛИ В ИНФРАСТРУКТУРЕ",
    "HUMAN-OPERATED RANSOMWARE (HUMOR)": "RANSOMWARE ПОД УПРАВЛЕНИЕМ ЧЕЛОВЕКА (HUMOR)",
    "AUTOMATED OR MASS-DISTRIBUTED RANSOMWARE": "АВТОМАТИЗИРОВАННОЕ И МАССОВО РАСПРОСТРАНЯЕМОЕ RANSOMWARE",
    "ENCRYPTIONLESS EXTORTION": "ВЫМОГАТЕЛЬСТВО БЕЗ ШИФРОВАНИЯ",
    "PSEUDO-RANSOMWARE AND WIPERS": "ПСЕВДО-RANSOMWARE И WIPER-АТАКИ",
    "MULTI-VECTOR EXTORTION CAMPAIGNS": "МНОГОВЕКТОРНЫЕ КАМПАНИИ ВЫМОГАТЕЛЬСТВА",
    "CRISIS COMMUNICATIONS AND PUBLIC RELATIONS": "КРИЗИСНЫЕ КОММУНИКАЦИИ И СВЯЗИ С ОБЩЕСТВЕННОСТЬЮ",
    "CTI FOR RANSOMWARE": "CTI ДЛЯ RANSOMWARE",
    "EMPLOYEE TRAINING AND AWARENESS": "ОБУЧЕНИЕ И ОСВЕДОМЛЁННОСТЬ СОТРУДНИКОВ",
    "IDENTITY, ACCESS, AND TIER-0 PROTECTION": "ЗАЩИТА ИДЕНТИЧНОСТЕЙ, ДОСТУПА И TIER-0",
    "RANSOMWARE-RESISTANT BACKUP STRATEGIES": "СТРАТЕГИИ РЕЗЕРВНОГО КОПИРОВАНИЯ, УСТОЙЧИВЫЕ К RANSOMWARE",
    "THE 3-2-1-1-0 BACKUP RULE": "ПРАВИЛО РЕЗЕРВНОГО КОПИРОВАНИЯ 3-2-1-1-0",
    "RANSOMWARE VERIFICATION INDICATORS": "ПРИЗНАКИ ДЛЯ ПРОВЕРКИ RANSOMWARE-ИНЦИДЕНТА",
    "THE INCIDENT COMMANDER ROLE": "РОЛЬ РУКОВОДИТЕЛЯ ИНЦИДЕНТА",
    "FRAMEWORK FOR RANSOMWARE SCOPING": "ФРЕЙМВОРК ОПРЕДЕЛЕНИЯ МАСШТАБА RANSOMWARE-ИНЦИДЕНТА",
    "DATA EXFILTRATION DETECTION STRATEGIES": "СТРАТЕГИИ ОБНАРУЖЕНИЯ ЭКСФИЛЬТРАЦИИ ДАННЫХ",
    "DECRYPTION POSSIBILITIES": "ВОЗМОЖНОСТИ РАСШИФРОВКИ",

    "IDENTITY AND ACCESS": "ИДЕНТИЧНОСТИ И ДОСТУП",
    "REMEDIATION STORAGE ACCOUNT И BUCKET": "ИСПРАВЛЕНИЕ STORAGE ACCOUNT И BUCKET",
    "IDENTITY AND ACCESS MANAGEMENT": "УПРАВЛЕНИЕ ИДЕНТИЧНОСТЯМИ И ДОСТУПОМ",
    "COMPUTE И WORKLOADS": "ВЫЧИСЛИТЕЛЬНЫЕ РЕСУРСЫ И WORKLOADS",
    "CLOUD INFRASTRUCTURE FOR FORENSIC WORKSTATIONS": "ОБЛАЧНАЯ ИНФРАСТРУКТУРА ДЛЯ ФОРЕНЗИК-СТАНЦИЙ",
    "SECURE, READ-ONLY LOG STORAGE": "ЗАЩИЩЁННОЕ ХРАНИЛИЩЕ ЖУРНАЛОВ ТОЛЬКО ДЛЯ ЧТЕНИЯ",
    "NETWORK LOGGING WITH VPC FLOW LOGS": "СЕТЕВОЕ ЖУРНАЛИРОВАНИЕ С VPC FLOW LOGS",
    "CONTAINERS AND SERVERLESS FOR FORENSIC TOOLING": "КОНТЕЙНЕРЫ И SERVERLESS ДЛЯ ФОРЕНЗИК-ИНСТРУМЕНТОВ",
    "AI-DRIVEN SOC OPERATIONS": "SOC-ОПЕРАЦИИ С ПОДДЕРЖКОЙ ИИ",
    "RUNTIME VISIBILITY ДЛЯ SERVERLESS И CONTAINERS": "НАБЛЮДАЕМОСТЬ ВРЕМЕНИ ВЫПОЛНЕНИЯ ДЛЯ SERVERLESS И КОНТЕЙНЕРОВ",
    "TOKEN-BASED ATTACKS": "АТАКИ НА ОСНОВЕ ТОКЕНОВ",
    "CLOUD-NATIVE FORENSICS": "ОБЛАЧНАЯ ФОРЕНЗИКА",

    "INCIDENT RESPONSE В OT ENVIRONMENTS": "РЕАГИРОВАНИЕ НА ИНЦИДЕНТЫ В OT-СРЕДАХ",
    "SAFETY КАК ОСНОВНАЯ МИССИЯ OT SECURITY": "БЕЗОПАСНОСТЬ КАК ОСНОВНАЯ ЦЕЛЬ OT-ЗАЩИТЫ",
    "SKILL SETS ДЛЯ OT DEFENDERS И RESPONDERS": "КОМПЕТЕНЦИИ OT-СПЕЦИАЛИСТОВ ПО ЗАЩИТЕ И РЕАГИРОВАНИЮ",
    "VENDOR SUPPORT И INDUSTRIAL SYSTEM LIFECYCLE CONSTRAINTS": "ПОДДЕРЖКА ПОСТАВЩИКА И ОГРАНИЧЕНИЯ ЖИЗНЕННОГО ЦИКЛА ПРОМЫШЛЕННЫХ СИСТЕМ",
    "INDUSTRIAL SYSTEM DESIGN И NETWORK ARCHITECTURE": "АРХИТЕКТУРА ПРОМЫШЛЕННЫХ СИСТЕМ И СЕТИ",
    "SECURITY CONTROL DESIGN И OPERATIONAL RISK TOLERANCE": "ПРОЕКТИРОВАНИЕ МЕР ЗАЩИТЫ И ДОПУСК ОПЕРАЦИОННОГО РИСКА",
    "WHY STANDARD IT CONTAINMENT CAN BE DANGEROUS IN OT": "ПОЧЕМУ СТАНДАРТНОЕ IT-СДЕРЖИВАНИЕ МОЖЕТ БЫТЬ ОПАСНЫМ В OT",
    "КОГДА IT CONTAINMENT САМ СОЗДАЕТ OT INCIDENT": "КОГДА IT-СДЕРЖИВАНИЕ САМО СОЗДАЁТ OT-ИНЦИДЕНТ",
    "COMMON OT ASSETS": "ТИПОВЫЕ OT-АКТИВЫ",
    "NON-TRADITIONAL OPERATING SYSTEM OT ASSETS": "OT-АКТИВЫ БЕЗ ТРАДИЦИОННОЙ ОПЕРАЦИОННОЙ СИСТЕМЫ",
    "TRADITIONAL OPERATING SYSTEM-BASED OT ASSETS": "OT-АКТИВЫ НА БАЗЕ ТРАДИЦИОННЫХ ОПЕРАЦИОННЫХ СИСТЕМ",
    "ПРЕИМУЩЕСТВА DAIR ДЛЯ OT INCIDENT RESPONSE": "ПРЕИМУЩЕСТВА DAIR ДЛЯ OT-РЕАГИРОВАНИЯ",
    "FIGHTING THROUGH THE ATTACK": "ПРОДОЛЖЕНИЕ БЕЗОПАСНОЙ РАБОТЫ ВО ВРЕМЯ АТАКИ",
    "VERIFY AND TRIAGE ДЛЯ OT": "ПРОВЕРКА И ТРИАЖ ДЛЯ OT",
    "LIVING-OFF-THE-LAND В MODERN OT ATTACKS": "LIVING-OFF-THE-LAND В СОВРЕМЕННЫХ OT-АТАКАХ",
    "TRADITIONAL VS NEW FORENSIC AREAS": "ТРАДИЦИОННЫЕ И НОВЫЕ ОБЛАСТИ ФОРЕНЗИКИ",
    "COMMON OT INCIDENT DATA SOURCES": "ОСНОВНЫЕ ИСТОЧНИКИ ДАННЫХ ОБ OT-ИНЦИДЕНТАХ",
    "ENGINEERING VALIDATION": "ИНЖЕНЕРНАЯ ПРОВЕРКА",
    "OT-SPECIFIC DEBRIEF QUESTIONS": "ВОПРОСЫ ДЛЯ РАЗБОРА OT-ИНЦИДЕНТА",

    "INCIDENT RESPONSE": "РЕАГИРОВАНИЕ НА ИНЦИДЕНТЫ",
    "INCIDENT MANAGEMENT": "УПРАВЛЕНИЕ ИНЦИДЕНТАМИ",
    "STEP-BY-STEP": "ПОШАГОВО",
    "SIDEBAR:": "ВРЕЗКА:",
    "CASE:": "ПРИМЕР:",
    "INTRODUCTION": "ВВЕДЕНИЕ",
    "PREPARE": "ПОДГОТОВКА",
    "DETECT": "ОБНАРУЖЕНИЕ",
    "VERIFY/TRIAGE": "ПРОВЕРКА И ТРИАЖ",
    "VERIFY AND TRIAGE": "ПРОВЕРКА И ТРИАЖ",
    "SCOPE": "ОПРЕДЕЛЕНИЕ МАСШТАБА",
    "CONTAINMENT": "СДЕРЖИВАНИЕ",
    "CONTAIN": "СДЕРЖИВАНИЕ",
    "ERADICATE": "ИСКОРЕНЕНИЕ",
    "RECOVER": "ВОССТАНОВЛЕНИЕ",
    "DEBRIEF": "РАЗБОР ИНЦИДЕНТА",
    "DOCUMENTATION": "ДОКУМЕНТИРОВАНИЕ",
    "INITIAL RISK ASSESSMENT": "НАЧАЛЬНАЯ ОЦЕНКА РИСКА",
    "STAKEHOLDER COMMUNICATION": "КОММУНИКАЦИЯ С ЗАИНТЕРЕСОВАННЫМИ СТОРОНАМИ",
    "PRACTICAL CONSIDERATIONS": "ПРАКТИЧЕСКИЕ АСПЕКТЫ",
    "KNOWING WHEN TO STOP": "КРИТЕРИИ ЗАВЕРШЕНИЯ",
    "ITERATION TRIGGERS": "ТРИГГЕРЫ НОВОЙ ИТЕРАЦИИ",
    "CLOUD-NATIVE DETECTION TOOLING": "ВСТРОЕННЫЕ ОБЛАЧНЫЕ СРЕДСТВА ОБНАРУЖЕНИЯ",
    "DETECTION TOOLING FOR AWS": "СРЕДСТВА ОБНАРУЖЕНИЯ В AWS",
    "DETECTION TOOLING FOR AZURE": "СРЕДСТВА ОБНАРУЖЕНИЯ В AZURE",
    "DETECTION TOOLING FOR GOOGLE CLOUD": "СРЕДСТВА ОБНАРУЖЕНИЯ В GOOGLE CLOUD",
    "CLOUD-SPECIFIC DEBRIEF QUESTIONS": "ВОПРОСЫ ДЛЯ РАЗБОРА ОБЛАЧНОГО ИНЦИДЕНТА",
    "AUTOMATED RESPONSE CAPABILITIES": "ВОЗМОЖНОСТИ АВТОМАТИЗИРОВАННОГО РЕАГИРОВАНИЯ",
    "MULTI-CLOUD ENVIRONMENTS": "МУЛЬТИОБЛАЧНЫЕ СРЕДЫ",
    "RANSOMWARE INTRODUCTION": "ВВЕДЕНИЕ В RANSOMWARE",
    "RANSOMWARE ATTACK TRENDS": "ТЕНДЕНЦИИ RANSOMWARE-АТАК",
    "INITIAL ACCESS TRENDS": "ТЕНДЕНЦИИ ПЕРВОНАЧАЛЬНОГО ДОСТУПА",
    "ATTACK DIFFERENTIATION": "РАЗЛИЧЕНИЕ ТИПОВ АТАК",
    "FINAL CONSIDERATIONS": "ЗАКЛЮЧИТЕЛЬНЫЕ СООБРАЖЕНИЯ",
    "RANSOMWARE-SPECIFIC METRICS": "МЕТРИКИ ДЛЯ RANSOMWARE-ИНЦИДЕНТОВ",
    "RANSOMWARE-SPECIFIC DEBRIEF QUESTIONS": "ВОПРОСЫ ДЛЯ РАЗБОРА RANSOMWARE-ИНЦИДЕНТА",
    "RECOVERY PLANNING AND PRIORITIZATION": "ПЛАНИРОВАНИЕ И ПРИОРИТИЗАЦИЯ ВОССТАНОВЛЕНИЯ",
    "DECRYPTED DOES NOT MEAN CLEAN": "РАСШИФРОВАНО НЕ ОЗНАЧАЕТ ОЧИЩЕНО",
    "WATCHING FOR ATTACKER RETURN": "НАБЛЮДЕНИЕ ЗА ВОЗВРАЩЕНИЕМ АТАКУЮЩЕГО",
    "COMMUNICATION DURING RECOVERY": "КОММУНИКАЦИЯ ВО ВРЕМЯ ВОССТАНОВЛЕНИЯ",
    "SAFETY": "БЕЗОПАСНОСТЬ",
    "ISLAND MODE": "АВТОНОМНЫЙ РЕЖИМ (ISLAND MODE)",
    "COMMON OT INCIDENT DATA SOURCES": "ОСНОВНЫЕ ИСТОЧНИКИ ДАННЫХ ОБ OT-ИНЦИДЕНТАХ",
    "TRADITIONAL VS NEW FORENSIC AREAS": "ТРАДИЦИОННЫЕ И НОВЫЕ ОБЛАСТИ ФОРЕНЗИКИ",
    "THE FIVE ICS CYBERSECURITY CRITICAL CONTROLS": "ПЯТЬ КРИТИЧЕСКИХ МЕР КИБЕРБЕЗОПАСНОСТИ ICS",
    "AI COSTS AND ACCESS": "СТОИМОСТЬ И ДОСТУП К ИИ",
    "OPPORTUNITIES AND CAUTIONS": "ВОЗМОЖНОСТИ И ОГРАНИЧЕНИЯ",
    "PROMPTING FOUNDATIONS": "ОСНОВЫ ФОРМИРОВАНИЯ ЗАПРОСОВ",
    "FOUNDATIONAL USE CASES": "БАЗОВЫЕ СЦЕНАРИИ ПРИМЕНЕНИЯ",
    "INTERMEDIATE USE CASES": "ПРОМЕЖУТОЧНЫЕ СЦЕНАРИИ ПРИМЕНЕНИЯ",
    "ADVANCED USE CASES": "РАСШИРЕННЫЕ СЦЕНАРИИ ПРИМЕНЕНИЯ",
    "OPERATIONAL CONSIDERATIONS": "ОПЕРАЦИОННЫЕ АСПЕКТЫ",
    "LOOKING FORWARD": "ЧТО ДАЛЬШЕ",
    "VERIFICATION IS NON-NEGOTIABLE": "ПРОВЕРКА ОБЯЗАТЕЛЬНА",
    "MODEL CONTEXT PROTOCOL FOR DEFENSIVE OPERATIONS": "MODEL CONTEXT PROTOCOL ДЛЯ ЗАЩИТНЫХ ОПЕРАЦИЙ",
    "SECURITY CONSIDERATIONS": "АСПЕКТЫ БЕЗОПАСНОСТИ",
    "HUMAN IN THE LOOP (HITL)": "ЧЕЛОВЕК В КОНТУРЕ (HITL)",
    "AUDITABILITY AND DOCUMENTATION": "АУДИРУЕМОСТЬ И ДОКУМЕНТИРОВАНИЕ",
    "STABLE PRINCIPLES": "УСТОЙЧИВЫЕ ПРИНЦИПЫ",
}

EXTERNAL_HEADING_MAP = {}

PHRASE_REPLACEMENTS = [
    ("incident response", "реагирование на инциденты"),
    ("Incident Response", "реагирование на инциденты"),
    ("incident management", "управление инцидентами"),
    ("Decision Makers", "лица, принимающие решения"),
    ("Decision-Makers", "лица, принимающие решения"),
    ("System Owner", "владелец системы"),
    ("System owner", "владелец системы"),
    ("Residual-Access Window", "окно остаточного доступа"),
    ("Initial Risk Assessment", "начальная оценка риска"),
    ("Cloud Incident Response", "реагирование на инциденты в облачной среде"),
    ("Control Plane", "плоскость управления"),
    ("Data Plane", "плоскость данных"),
    ("Runtime visibility", "наблюдаемость времени выполнения"),
    ("Multi-cloud visibility", "сквозная видимость multi-cloud"),
]

def load_external_heading_map(repo_root: Path):
    global EXTERNAL_HEADING_MAP
    root = repo_root / "books" / BOOK_ID / "translation" / "ru"
    merged = {}
    for p in sorted(root.glob("V2-HEADING-MAP*.yaml")):
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        raw = data.get("headings") or {}
        for k, v in raw.items():
            merged[str(k).upper()] = str(v)
    EXTERNAL_HEADING_MAP = merged


def normalize_heading_text(text: str) -> str:
    original = text
    key = text.strip()
    upper = key.upper()
    if upper in EXTERNAL_HEADING_MAP:
        return EXTERNAL_HEADING_MAP[upper]
    if upper in HEADING_REPLACEMENTS:
        return HEADING_REPLACEMENTS[upper]
    out = key
    for src, dst in PHRASE_REPLACEMENTS:
        out = out.replace(src, dst)
    # Keep code/generated-content section markers stable if translation would be ambiguous.
    out = re.sub(r"\bSTEP (\d+)\b", r"Шаг \1", out, flags=re.I)
    return out if out else original

def find_mixed_heading_candidates(text: str):
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("~~~") or line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not re.match(r"^#{1,4}\s+", line):
            continue
        title = re.sub(r"^#{1,4}\s+", "", line).strip()
        if re.match(r"^(Рисунок|Листинг|Listing|Таблица|Table)\s+", title, re.I):
            continue
        latin = sum(ch.isascii() and ch.isalpha() for ch in title)
        cyr = sum(("А" <= ch <= "я") or ch in "Ёё" for ch in title)
        if latin >= 8 and latin > max(4, cyr * 0.45):
            out.append(title)
    return out


def inject_project_visual(text: str, image_rel: str, chapter: int) -> str:
    lines = text.splitlines()
    insert_at = 1
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 1
            break
    block = [
        "",
        f"![Дополнительная схема к главе {chapter}]({image_rel})",
        "",
        f"*Дополнительная схема biblioteka-vsp к главе {chapter}; не является оригинальной иллюстрацией книги.*",
        "",
    ]
    return "\n".join(lines[:insert_at] + block + lines[insert_at:]).strip() + "\n"


def normalize_body_v2(text: str) -> str:
    text = html.unescape(text.replace("\r\n", "\n"))
    text = text.replace("&#x20;", " ")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    lines = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            marks, title = m.groups()
            title = normalize_heading_text(title)
            line = f"{marks} {title}"
        lines.append(line)
    text = "\n".join(lines)

    text = re.sub(
        r"^THIRD_PARTY_REVIEW_REQUIRED\s*[—-]?\s*(.*)$",
        lambda m: "> **Иллюстрация не воспроизводится:** требуется отдельная проверка прав на сторонний визуальный материал."
                  + (f" {m.group(1).strip()}" if m.group(1).strip() else ""),
        text,
        flags=re.MULTILINE,
    )
    text = text.replace("THIRD_PARTY_REVIEW_REQUIRED", "**Иллюстрация не воспроизводится:** требуется отдельная проверка прав на сторонний визуальный материал.")
    text = text.replace("RAG_MISS", "пропуск в извлечённом тексте источника")
    return text.strip() + "\n"

def audit_and_assemble(repo_root: Path, out_dir: Path):
    load_external_heading_map(repo_root)
    tr_root = repo_root / "books" / BOOK_ID / "translation" / "ru"
    chapters_dir = tr_root / "chapters"
    chapter_files = sorted(
        [p for p in chapters_dir.glob("chapter-*.md") if not p.name.endswith(".qa.md")],
        key=chapter_num,
    )
    qa_files = {chapter_num(p): p for p in chapters_dir.glob("chapter-*.qa.md")}
    problems = []
    rows = []
    parts = []
    original_third_party = 0
    v2_third_party = 0
    mixed_heading_candidates = []
    project_visuals_included = 0

    if [chapter_num(p) for p in chapter_files] != list(range(1, 21)):
        problems.append("chapter sequence mismatch")

    for p in chapter_files:
        n = chapter_num(p)
        raw = p.read_text(encoding="utf-8")
        meta, body = split_frontmatter(raw)
        q = qa_files.get(n)
        qmeta = {}
        if q:
            qmeta, _ = split_frontmatter(q.read_text(encoding="utf-8"))
        if meta.get("translation_status") != "ACCEPTED":
            problems.append(f"chapter {n}: translation status is not ACCEPTED")
        if qmeta.get("qa_status") != "ACCEPTED":
            problems.append(f"chapter {n}: QA status is not ACCEPTED")
        if "[Needs confirmation]" in body:
            problems.append(f"chapter {n}: unexpected [Needs confirmation]")
        original_third_party += body.count("THIRD_PARTY_REVIEW_REQUIRED")
        repaired = normalize_body_v2(body)
        v2_third_party += repaired.count("требуется отдельная проверка прав на сторонний визуальный материал")

        note_root = repo_root / "books" / BOOK_ID / "notes" / "chapters"
        matches = sorted(note_root.glob(f"chapter-{n:02d}-*/visual-cheatsheet.svg"))
        if matches:
            visuals_dir = out_dir / "visuals"
            visuals_dir.mkdir(parents=True, exist_ok=True)
            visual_out = visuals_dir / f"chapter-{n:02d}-visual-cheatsheet.svg"
            shutil.copy2(matches[0], visual_out)
            repaired = inject_project_visual(repaired, f"visuals/{visual_out.name}", n)
            project_visuals_included += 1

        for heading in find_mixed_heading_candidates(repaired):
            mixed_heading_candidates.append({"chapter": n, "heading": heading})

        parts.append(repaired)
        title = next((l.lstrip("# ").strip() for l in repaired.splitlines() if l.startswith("# ")), p.stem)
        rows.append({"chapter": n, "file": p.name, "title": title})

    afterword = tr_root / "afterword.md"
    afterword_qa = tr_root / "afterword.qa.md"
    if not afterword.exists() or not afterword_qa.exists():
        problems.append("afterword or QA missing")
        abody = ""
    else:
        ameta, abody = split_frontmatter(afterword.read_text(encoding="utf-8"))
        aqmeta, _ = split_frontmatter(afterword_qa.read_text(encoding="utf-8"))
        if ameta.get("translation_status") != "ACCEPTED":
            problems.append("afterword translation status is not ACCEPTED")
        if aqmeta.get("qa_status") != "ACCEPTED":
            problems.append("afterword QA status is not ACCEPTED")
        original_third_party += abody.count("THIRD_PARTY_REVIEW_REQUIRED")
        abody = normalize_body_v2(abody)

    if project_visuals_included != 20:
        problems.append(f"project visual count mismatch: expected=20, got={project_visuals_included}")

    if v2_third_party != original_third_party:
        problems.append(
            f"third-party marker preservation mismatch: source={original_third_party}, v2={v2_third_party}"
        )

    audit = {
        "book_id": BOOK_ID,
        "edition": "ru-v2-repair",
        "status": "ACCEPTED" if not problems else "BLOCKED",
        "chapters": rows,
        "third_party_markers_source": original_third_party,
        "third_party_callouts_v2": v2_third_party,
        "project_visuals_included": project_visuals_included,
        "mixed_heading_candidate_count": len(mixed_heading_candidates),
        "mixed_heading_candidates": mixed_heading_candidates,
        "problems": problems,
        "chapter_analysis_workflow": "BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.2 -> BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.6",
        "workflow_provenance": "RETROFIT_VERIFIED_COMPATIBILITY",
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "dynamic-incident-response-ru-v2-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if problems:
        raise SystemExit("RU v2 audit BLOCKED:\n- " + "\n- ".join(problems))

    toc = ["# Оглавление", ""] + [f"- {r['title']}" for r in rows] + ["- Послесловие"]
    header = f"""---
title: "{BOOK_TITLE_RU}"
subtitle: "{BOOK_SUBTITLE_RU} - неофициальный русский перевод, редакция v2"
author: "{AUTHOR}"
date: "{YEAR}"
lang: ru-RU
---

{chr(10).join(toc)}

# Сведения об издании

**Оригинал:** *{ORIGINAL_TITLE}*  
**Автор:** {AUTHOR}  
**Издатель оригинала:** SANS Institute, {YEAR}  
**Лицензия основного авторского материала:** {LICENSE}  
**Лицензия:** https://creativecommons.org/licenses/by/4.0/

Это **неофициальный русский перевод**. Редакция v2 выполнена как редакторский ремонт принятого перевода глав 1-20 и послесловия: нормализация заголовков, терминологии и типографики без замены canonical English RAG.

Аналитические материалы глав проверены на совместимость с:
`BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.2 -> BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.6`.

Сторонние визуальные материалы не воспроизводятся без отдельной проверки прав. На их месте сохраняются подписи и явные пометки.

"""
    md = header + "\n\n".join(parts) + "\n\n" + abody

    glossary_path = tr_root / "glossary.yaml"
    if glossary_path.exists():
        gd = yaml.safe_load(glossary_path.read_text(encoding="utf-8")) or {}
        entries = gd.get("entries") or gd.get("terms") or []
        if isinstance(entries, list) and entries:
            gl = ["# Приложение. Глоссарий", ""]
            for e in entries:
                if not isinstance(e, dict):
                    continue
                src = str(e.get("source", "")).strip()
                ru = str(e.get("ru", "")).strip()
                note = str(e.get("context_note", "")).replace("\n", " ").strip()
                if not src:
                    continue
                item = f"- **{src}**"
                if ru:
                    item += f" - {ru}"
                if note:
                    item += f". {note}"
                gl.append(item)
            md += "\n\n" + "\n".join(gl) + "\n"

    md_path = out_dir / "dynamic-incident-response-ru-v2.md"
    md_path.write_text(md, encoding="utf-8")
    return md_path, audit

def run_pandoc(md_path: Path, out_dir: Path):
    ref = out_dir / "reference-v2.docx"
    build_reference_docx(ref)
    docx = out_dir / "dynamic-incident-response-ru-v2-a4.docx"
    subprocess.run([
        "pandoc", str(md_path),
        "--from", "markdown+yaml_metadata_block",
        "--to", "docx",
        "--reference-doc", str(ref),
        "--output", str(docx),
    ], check=True)
    return docx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--out-dir", default="build/dynamic-ir-ru-v2")
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    md, audit = audit_and_assemble(repo_root, out_dir)
    docx = run_pandoc(md, out_dir)
    print(json.dumps({"status": audit["status"], "markdown": str(md), "docx": str(docx)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
