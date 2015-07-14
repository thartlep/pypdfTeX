import os

def merge_multiple_pdfs_onto_one_page(outputfilename,inputfilenames,numcol,numrow,orientation='landscape',leave_temporary_files=False):

  for filename in inputfilenames:
     print filename

  minipage_width = 0.95/numcol

  # define latex commands
  texfilelines_start_document = []
  if orientation == 'landscape':
     texfilelines_start_document.append(r'\documentclass[landscape]{report}')
  else:
     texfilelines_start_document.append(r'\documentclass[]{report}')
  texfilelines_start_document.append(r'\usepackage[margin=0.5in]{geometry}')
  texfilelines_start_document.append(r'\usepackage{subfigure}')
  texfilelines_start_document.append(r'\usepackage[pdftex]{graphicx}')
  texfilelines_start_document.append(r'\usepackage{grffile}')
  texfilelines_start_document.append(r'\begin{document}')

  texfilelines_start_figure = []
  texfilelines_start_figure.append(r'\begin{figure}[ht]')
#  texfilelines_start_figure.append(r'   \centering')

  texfilelines_start_minipage = []
  texfilelines_start_minipage.append(r'   \begin{minipage}{'+str(minipage_width)+'\linewidth}')

  texfilelines_include_graphics_begin = r'      \includegraphics[width=\linewidth]{{'
  texfilelines_include_graphics_end   = '}}'

  texfilelines_end_minipage = []
  texfilelines_end_minipage.append(r'   \end{minipage}')

  texfilelines_end_figure = []
  texfilelines_end_figure.append(r'\end{figure}')

  texfilelines_end_document = []
  texfilelines_end_document.append(r'\end{document}')

  # generate tex file
  f=open(outputfilename[:-4]+'.tex','w')

  for line in texfilelines_start_document:
    f.write(line+'\n')

  plot_counter = 0
  minipage_counter = 0
  for i in range(0,len(inputfilenames)):
     inputfilename = inputfilenames[i]

     # new figure environment 
     if minipage_counter == 0 and plot_counter == 0:
        for line in texfilelines_start_figure:
           f.write(line+'\n')

     # new minipage
     if plot_counter == 0:
        for line in texfilelines_start_minipage:
           f.write(line+'\n')

     f.write(texfilelines_include_graphics_begin+inputfilename+texfilelines_include_graphics_end+'\n')
     plot_counter += 1
     if plot_counter == numrow:
        minipage_counter += 1

     # end minipage
     if plot_counter == numrow or i == len(inputfilenames)-1:
        plot_counter = 0
        for line in texfilelines_end_minipage:
           f.write(line+'\n')

     # end figure environment
     if minipage_counter == numcol or i == len(inputfilenames)-1:
        minipage_counter = 0
        for line in texfilelines_end_figure:
           f.write(line+'\n')

  for line in texfilelines_end_document:
    f.write(line+'\n')

  f.close()


  # run pdflatex
  os.system('pdflatex '+outputfilename[:-4]+'.tex\n')

  # clean up
  if not leave_temporary_files:
    os.system('rm '+outputfilename[:-4]+'.tex\n')
    os.system('rm '+outputfilename[:-4]+'.aux\n')
    os.system('rm '+outputfilename[:-4]+'.log\n')

