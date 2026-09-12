type QueuePaginationProps = {
  page: number;
  pages: number;
  onChange: (page: number) => void;
};

export function QueuePagination({ page, pages, onChange }: QueuePaginationProps) {
  if (pages <= 1) return null;

  return (
    <nav aria-label="Queue pages" className="pagination">
      <button disabled={page <= 1} onClick={() => onChange(page - 1)} type="button">
        Previous
      </button>
      <small>Page {page} of {pages}</small>
      <button disabled={page >= pages} onClick={() => onChange(page + 1)} type="button">
        Next
      </button>
    </nav>
  );
}
