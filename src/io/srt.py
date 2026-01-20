def parse_srt(srt_file: str) -> dict:
    '''
    Parse the SRT file and extract frame data.
    Args:
        srt_file (str): The file path to the SRT file.
    Returns:
        dict: A dictionary containing frame data.
    '''
    print("Parsing SRT file...")

    frame_data = {}
    with open(srt_file, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = content.split("\n\n")
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        frame_no = lat = lon = alt = None
        for line in lines:
            if "FrameCnt:" in line:
                try:
                    frame_no = int(line.split("FrameCnt:")[1].split(",")[0].strip())
                except:
                    continue
            if "[" in line and "]" in line:
                parts = line.split("[")
                for part in parts[1:]:
                    part = part.strip(" ]")
                    if "latitude:" in part:
                        try:
                            lat = float(part.split(":")[1].strip())
                        except:
                            pass
                    elif "longitude:" in part:
                        try:
                            lon = float(part.split(":")[1].strip())
                        except:
                            pass
                    elif "rel_alt:" in part:
                        try:
                            alt_str = part.split("rel_alt:")[1].split("abs_alt:")[0].strip()
                            alt = float(alt_str)
                        except:
                            pass
        if frame_no and lat is not None and lon is not None and alt is not None:
            frame_data[frame_no] = (lat, lon, alt)
            print(f"Parsed metadata for frame {frame_no}", end="\r")
            
    print(f"Successfully parsed metadata for {len(frame_data)} frames")

    return frame_data
