import subprocess


subprocess.run(["mkinit", "src/ai_assistant_parsers_core/parsers", "--recursive", "-w", "--nomods", "--relative", "--black"])
subprocess.run(["mkinit", "src/ai_assistant_parsers_core/refiners", "--recursive", "-w", "--nomods", "--relative", "--black"])
subprocess.run(["mkinit", "src/ai_assistant_parsers_core/cli", "--recursive", "-w", "--nomods", "--relative", "--black"])
subprocess.run(["mkinit", "src/ai_assistant_parsers_core/fetchers", "--recursive", "-w", "--nomods", "--relative", "--black"])
