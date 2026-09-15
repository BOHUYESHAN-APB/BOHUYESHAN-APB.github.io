import { readFileSync } from "node:fs";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkRehype from "remark-rehype";
import { visit } from "unist-util-visit";

let called = 0;
function remarkMermaidPlaceholder() {
  return tree => {
    called++;
    visit(tree, "code", node => {
      if (node.lang === "mermaid") {
        console.log("FOUND mermaid code node, lang =", JSON.stringify(node.lang));
        node.type = "html";
        node.value = `<div class="mermaid-block" data-source="${encodeURIComponent(node.value)}"></div>`;
      }
    });
  };
}

const md = readFileSync(
  "src/content/posts/2026/09/12/2026-09-12-08-生信图表大全第六篇-用真实公开数据画的22张图.md",
  "utf8"
);

const processor = unified()
  .use(remarkParse)
  .use(remarkMermaidPlaceholder)
  .use(remarkRehype);

const result = await processor.run(processor.parse(md));
console.log("plugin visits:", called);
console.log("html nodes with mermaid-block:", JSON.stringify(result).includes("mermaid-block"));
