export default function StatusBadge({ view, title }) {
  return (
    <span className={`badge badge--${view.tone}`} title={title}>
      {view.label}
    </span>
  );
}
