/* Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
   file LICENSE.  */

#ifndef __qAppStyle_h
#define __qAppStyle_h

// SlicerSALT includes
#include "qSlicerSALTAppExport.h"

// Slicer includes
#include "qSlicerStyle.h"

class Q_SLICERSALT_APP_EXPORT qAppStyle
  : public qSlicerStyle
{
  Q_OBJECT
public:
  /// Superclass typedef
  typedef qSlicerStyle Superclass;

  /// Constructors
  qAppStyle();
  virtual ~qAppStyle();

  /// Reimplemented to customize colors.
  /// \sa QStyle::standardPalette()
  virtual QPalette standardPalette() const;

  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawComplexControl()
  void drawComplexControl(ComplexControl control,
                          const QStyleOptionComplex* option,
                          QPainter* painter,
                          const QWidget* widget = 0)const;
  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawControl()
  virtual void drawControl(ControlElement element,
                           const QStyleOption* option,
                           QPainter* painter,
                           const QWidget* widget = 0 )const;

  /// Reimplemented to apply custom palette to widgets
  /// \sa QStyle::drawPrimitive()
  virtual void drawPrimitive(PrimitiveElement element,
                             const QStyleOption* option,
                             QPainter* painter,
                             const QWidget* widget = 0 )const;

  /// Tweak the colors of some widgets.
  virtual QPalette tweakWidgetPalette(QPalette palette,
                                      const QWidget* widget)const;

  /// Reimplemented to apply styling to widgets.
  /// \sa QStyle::polish()
  virtual void polish(QWidget* widget);
  using Superclass::polish;
};

#endif
