function img = ltsa_write(ltsa, filename, cmap)

% cmap: handle to colormap function, ie @jet

if nargin < 3
    cmap = @jet;
end

% scale ltsa such that 0 <= ltsa <= 255
ltsa = ltsa - min(min(ltsa));
ltsa = ltsa * (255 / max(max(ltsa)));
ltsa = uint8(ltsa);
ltsa(ltsa < 1) = 1;

map = cmap(256);

img = uint8(zeros(size(ltsa)));

for i = 1:3
    submap = map(:,i);
    img(:,:,i) = flipud( submap(ltsa) * 255 );   
end

if nargin > 1
    imwrite(img, filename);
end

if nargout == 0
    img = 1;
end

end
