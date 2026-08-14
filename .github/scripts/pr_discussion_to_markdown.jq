# Converts the GraphQL PR-discussion dump (see the "Fetch PR discussion" step in
# .github/workflows/claude_pr_review.yml) into a markdown digest for the Claude
# review prompt. Comment bodies are blockquoted so that untrusted user text stays
# visually separated from the document structure.

def login(a): if a == null then "(deleted user)" else a.login end;
def body_quote(s):
  if s == null or s == "" then "> (no text)"
  else s | gsub("\r"; "") | split("\n") | map("> " + .) | join("\n")
  end;

.data.repository.pullRequest as $pr
| ($pr.reviews.nodes | map(select(.state != "PENDING"))) as $reviews
| $pr.reviewThreads.nodes as $threads
| $pr.comments.nodes as $comments
| [
    "# Discussion already posted on this pull request",
    "",
    "## Submitted reviews",
    (if ($reviews | length) == 0 then "(none)"
     else $reviews[]
       | "### \(login(.author)) — \(.state) (\(.submittedAt))",
         body_quote(.body),
         ""
     end),
    "## Inline comment threads",
    (if ($threads | length) == 0 then "(none)"
     else $threads[]
       | ("### `\(.path)`"
           + (if .line != null then " line \(.line)" else "" end)
           + " — "
           + (if .isResolved then "RESOLVED" else "UNRESOLVED" end)
           + (if .isOutdated then " (outdated)" else "" end)),
         (.comments.nodes[]
           | "**\(login(.author))** (\(.createdAt)):",
             body_quote(.body),
             ""),
         ""
     end),
    "## Conversation comments",
    (if ($comments | length) == 0 then "(none)"
     else $comments[]
       | "### \(login(.author)) (\(.createdAt))",
         body_quote(.body),
         ""
     end)
  ]
+ (if $pr.reviews.pageInfo.hasNextPage
      or $pr.reviewThreads.pageInfo.hasNextPage
      or $pr.comments.pageInfo.hasNextPage
      or ([$threads[].comments.pageInfo.hasNextPage] | any)
   then ["",
         ("WARNING: This digest is truncated; only the first 100 items per "
          + "section are included.")]
   else [] end)
| .[]
