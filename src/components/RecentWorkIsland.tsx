import {useMemo, useRef, useState} from "preact/hooks";

type WorkItem ={
    id:string;
    title:string;
    creator:string;
    type:string;
    time:string;
    class_size:string;
};

type Props = {
    recentWork: WorkItem[];
    distinctTypes: string[];
}


const truncate = (value:string, max=100) =>
    value.length > max ? `${value.slice(0,max)} ...` : value;

export default function RecentWorkIsland({recentWork, distinctTypes}:Props){
    const [selectedType, setSelectedType] = useState("All");
    const carouselRef = useRef<HTMLDivElement>(null);

    const filteredWork = useMemo(
        ()=>(selectedType === "All" ? recentWork : recentWork.filter((item)=>item.type === selectedType)),
        [recentWork, selectedType]
    );


    const scrollCards = (direction:number) => {
        const container = carouselRef.current;
        if(!container || !container.firstElementChild) return;

        const cardWidth = (container.firstElementChild as HTMLElement).offsetWidth + 32;
        container.scrollBy({ left:direction * cardWidth, behavior: "smooth"});
    };

    return (
        <div>
            <div className="filter-row">
                <label htmlFor="typeFilter" className="filter-label">Filter by type</label>
                <select
                    id="typeFilter"
                    className="type-select"
                    value={selectedType}
                    onChange={(e)=>setSelectedType((e.target as HTMLSelectElement).value)}
                    aria-label="Filter recent work by type"
                >
                    <option value="All">All types</option>
                    {distinctTypes.map((type)=>(
                        <option value={type} key={type}>{type}</option>
                    ))}
                </select>
            </div>

            <div className="carousel-wrapper">
                <button className="nav-btn" onClick={()=>scrollCards(-1)} aria-label="Scroll left">←</button>

                <div className="carousel" id="carousel" ref={carouselRef}>
                    {filteredWork.map((item)=>(
                        <div className="card" key={item.id}>
                            <h3>{item.title}</h3>
                            <p><strong>Creator:</strong>{item.creator}</p>
                            <p><strong>Type:</strong>{item.type}</p>
                            <p><strong>Time:</strong>{truncate(item.time)}</p>
                            <p><strong>Class size:</strong>{truncate(item.class_size)}</p>
                            <a className="learn-more-btn" href={`/recent-work/${item.id}`}>Learn more →</a>
                        </div>
                    ))}
                </div>
                <button className="nav-btn" onClick={()=>scrollCards(1)} aria-label="Scroll right">→</button>
            </div>
        </div>
    )
}