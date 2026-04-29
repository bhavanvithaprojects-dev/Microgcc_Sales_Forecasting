export default function DateRangePicker({ value, onChange }) {
  return (
    <input 
      type="date" 
      className="filter-input" 
      value={value}
      onChange={(e) => onChange && onChange(e.target.value)}
    />
  );
}